/**
 * Analysis E: conformance of the browser-side validation and parsing logic.
 *
 * The script imports the real functions from
 * evo2-frontend/src/utils/genome-api.ts and the real Zod schema from
 * evo2-frontend/src/app/api/analyze/route.ts, so nothing is re-implemented.
 * It then
 *   1. executes the canonical case matrix (docs/analysis/validation_cases.json)
 *      against the Zod schema,
 *   2. retrieves live ClinVar records for BRCA1,
 *   3. reproduces the position and variant parsing that the browser
 *      components perform, and
 *   4. checks the assembly consistency of the ClinVar coordinate that the
 *      browser forwards to the scoring endpoint.
 *
 * Run from the repository root:
 *   node --experimental-strip-types docs/analysis/e_clinvar_conformance.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, "..", "..");
const FRONTEND = path.join(REPO, "evo2-frontend");
const line = (s = "") => console.log(s);

/* ------------------------------------------------------------------ *
 * 1. Load the real frontend helpers (type-stripped copy, no next/font) *
 * ------------------------------------------------------------------ */
const apiSrc = fs
  .readFileSync(path.join(FRONTEND, "src/utils/genome-api.ts"), "utf8")
  .replace(/^import \{ Viaoda_Libre \} from "next\/font\/google";\s*$/m, "");
const tmpTs = path.join(FRONTEND, ".analysis-genome-api.ts");
fs.writeFileSync(tmpTs, apiSrc, "utf8");
const api = await import(pathToFileURL(tmpTs).href);
fs.unlinkSync(tmpTs);

/* ------------------------------------------------------------------ *
 * 2. Extract the real Zod schema from the Next.js route handler        *
 * ------------------------------------------------------------------ */
const routeSrc = fs.readFileSync(
  path.join(FRONTEND, "src/app/api/analyze/route.ts"),
  "utf8",
);
const start = routeSrc.indexOf("const schema = z");
const end = routeSrc.indexOf("\n\nexport async function POST");
if (start < 0 || end < 0) throw new Error("could not locate the Zod schema");
const schemaSrc = routeSrc.slice(start, end);
const tmpSchemaTs = path.join(FRONTEND, ".analysis-analyze-schema.ts");
fs.writeFileSync(
  tmpSchemaTs,
  `import { z } from "zod";\n${schemaSrc}\nexport default schema;\n`,
  "utf8",
);
const { default: schema } = await import(pathToFileURL(tmpSchemaTs).href);
fs.unlinkSync(tmpSchemaTs);

/* ------------------------------------------------------------------ *
 * 3. Canonical validation matrix against the Zod schema                *
 * ------------------------------------------------------------------ */
const spec = JSON.parse(
  fs.readFileSync(path.join(REPO, "docs/analysis/validation_cases.json"), "utf8"),
);
function expand(value) {
  if (value && typeof value === "object" && "$repeat" in value) {
    const r = value["$repeat"];
    return (r.char ?? "A").repeat(r.count ?? 0) + (r.suffix ?? "");
  }
  return value;
}
const zodResults = spec.cases.map((c) => {
  const payload = {
    ...spec.base,
    ...Object.fromEntries(
      Object.entries(c.payload).map(([k, v]) => [k, expand(v)]),
    ),
  };
  const r = schema.safeParse(payload);
  const got = r.success ? "accept" : "reject";
  return {
    name: c.name,
    expect: c.expect,
    got,
    ok: got === c.expect,
    detail: r.success
      ? ""
      : r.error.issues.map((i) => i.message).join("; ").slice(0, 200),
    payload,
  };
});

line("=".repeat(78));
line("E.1  Zod validation matrix (Next.js route handler)");
line("=".repeat(78));
let zpass = 0;
for (const r of zodResults) {
  if (r.ok) zpass++;
  else line(`  NON-CONFORMING ${r.name}: expected ${r.expect}, got ${r.got}`);
}
line(`cases executed : ${zodResults.length}`);
line(`conforming    : ${zpass}/${zodResults.length}`);

fs.writeFileSync(
  path.join(REPO, "docs/analysis/e_zod_cases.json"),
  JSON.stringify({ layer: "zod", cases: zodResults.length, conforming: zpass, verdicts: zodResults }, null, 2),
);

/* ------------------------------------------------------------------ *
 * 4. Live ClinVar records for BRCA1                                     *
 * ------------------------------------------------------------------ */
const EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils";
async function getJSON(url) {
  const r = await fetch(url, { headers: { "User-Agent": "evo2serve-paper/1.0" } });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.json();
}
const term = "BRCA1[gene]";
const search = await getJSON(
  `${EU}/esearch.fcgi?db=clinvar&term=${encodeURIComponent(term)}&retmode=json&retmax=300`,
);
const ids = search.esearchresult.idlist;
const summary = await getJSON(
  `${EU}/esummary.fcgi?db=clinvar&id=${ids.join(",")}&retmode=json`,
);
const records = [];
for (const id of summary.result.uids) {
  const v = summary.result[id];
  const locs = {};
  for (const vs of v.variation_set ?? [])
    for (const L of vs.variation_loc ?? [])
      locs[L.assembly_name] = {
        start: Number(L.start),
        stop: Number(L.stop),
        status: L.status,
      };
  records.push({
    id,
    title: v.title ?? "",
    obj_type: v.obj_type ?? "",
    location_sort: v.location_sort ?? "",
    chr_sort: v.chr_sort ?? "",
    classification: v.germline_classification?.description ?? "",
    review_status: v.germline_classification?.review_status ?? "",
    locs,
  });
}

/* ------------------------------------------------------------------ *
 * 5. Reproduce the browser-side position extraction                    *
 * ------------------------------------------------------------------ */
function frontendLocation(r) {
  return r.location_sort ? parseInt(r.location_sort).toLocaleString() : "Unknown";
}
const posOutcomes = { numeric: 0, nan: 0, unknown: 0 };
for (const r of records) {
  const loc = frontendLocation(r);
  if (loc === "Unknown") posOutcomes.unknown++;
  else if (Number.isNaN(parseInt(loc.replaceAll(",", "")))) posOutcomes.nan++;
  else posOutcomes.numeric++;
}

/* ------------------------------------------------------------------ *
 * 6. Assembly consistency of the forwarded coordinate                   *
 * ------------------------------------------------------------------ */
let both = 0;
let sameAs38 = 0;
let sameAs37 = 0;
const offsets = [];
for (const r of records) {
  const ls = parseInt(r.location_sort);
  const p38 = r.locs["GRCh38"]?.start;
  const p37 = r.locs["GRCh37"]?.start;
  if (ls === p38) sameAs38++;
  if (ls === p37) sameAs37++;
  if (p38 != null && p37 != null) {
    both++;
    offsets.push(p38 - p37);
  }
}
offsets.sort((a, b) => a - b);
const offMin = offsets.length ? offsets[0] : null;
const offMax = offsets.length ? offsets[offsets.length - 1] : null;
const offMedian = offsets.length ? offsets[Math.floor(offsets.length / 2)] : null;
const offUnique = [...new Set(offsets)];

/* ------------------------------------------------------------------ *
 * 7. Title parsing                                                      *
 * ------------------------------------------------------------------ */
function isAnalyzableVariant(v) {
  const vt = v.variation_type?.toLowerCase() ?? "";
  if (vt.includes("single nucleotide")) return true;
  if (api.isDelinsClinvarVariant(v)) return api.inferDelinsFromTitle(v.title) != null;
  if (api.isInsertionClinvarVariant(v) && !api.isDeletionClinvarVariant(v))
    return api.inferInsertedSequenceFromTitle(v.title) != null;
  if (vt.includes("deletion") || api.isDeletionClinvarVariant(v)) return true;
  return /(\w)>(\w)/.test(v.title);
}
const toVariant = (r) => ({
  clinvar_id: r.id,
  title: r.title,
  variation_type: r.obj_type
    .split(" ")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(" "),
  classification: r.classification,
  location: frontendLocation(r),
});
const counts = {
  total: records.length,
  single_nucleotide: 0,
  deletion: 0,
  insertion: 0,
  delins: 0,
  other: 0,
  analyzable: 0,
  analyzable_with_usable_position: 0,
};
const details = [];
for (const r of records) {
  const v = toVariant(r);
  const t = v.variation_type.toLowerCase();
  if (t.includes("single nucleotide")) counts.single_nucleotide++;
  else if (api.isDelinsClinvarVariant(v)) counts.delins++;
  else if (api.isInsertionClinvarVariant(v) && !api.isDeletionClinvarVariant(v)) counts.insertion++;
  else if (api.isDeletionClinvarVariant(v)) counts.deletion++;
  else counts.other++;
  const analyzable = isAnalyzableVariant(v);
  if (analyzable) counts.analyzable++;
  const pos = parseInt(v.location.replaceAll(",", ""));
  const posOk = !Number.isNaN(pos) && pos > 0;
  if (analyzable && posOk) counts.analyzable_with_usable_position++;
  let derived = null;
  if (api.isDelinsClinvarVariant(v)) {
    const p = api.inferDelinsFromTitle(v.title);
    derived = p ? { kind: "delins", deletionLength: p.deletionLength, inserted: p.inserted } : null;
  } else if (api.isInsertionClinvarVariant(v) && !api.isDeletionClinvarVariant(v)) {
    const s = api.inferInsertedSequenceFromTitle(v.title);
    derived = s ? { kind: "insertion", inserted: s } : null;
  } else if (api.isDeletionClinvarVariant(v)) {
    derived = { kind: "deletion", deletionLength: api.inferDeletionLengthFromTitle(v.title) };
  } else {
    const m = v.title.match(/(\w)>(\w)/);
    if (m) derived = { kind: "snv", ref: m[1], alt: m[2] };
  }
  details.push({
    id: r.id, title: v.title, obj_type: r.obj_type,
    location_sort: r.location_sort, frontend_location: v.location,
    position_usable: posOk, analyzable, derived,
  });
}
const derivedKinds = {};
for (const d of details) {
  const k = d.derived ? d.derived.kind : "none";
  derivedKinds[k] = (derivedKinds[k] ?? 0) + 1;
}

line("");
line("=".repeat(78));
line("E.2  Live ClinVar records for BRCA1");
line("=".repeat(78));
line(`records fetched (esearch retmax=300) : ${records.length}`);
const objTypes = {};
for (const r of records) objTypes[r.obj_type] = (objTypes[r.obj_type] ?? 0) + 1;
for (const [k, v] of Object.entries(objTypes).sort((a, b) => b[1] - a[1]))
  line(`  ${k.padEnd(34)} ${v}`);
const review = {};
for (const r of records) review[r.review_status] = (review[r.review_status] ?? 0) + 1;
line("review status distribution:");
for (const [k, v] of Object.entries(review).sort((a, b) => b[1] - a[1]))
  line(`  ${k.padEnd(52)} ${v}`);

line("");
line("=".repeat(78));
line("E.3  Assembly consistency of the forwarded coordinate");
line("=".repeat(78));
line(`records with a GRCh38 and a GRCh37 location    : ${both}`);
line(`location_sort equals the GRCh38 start             : ${sameAs38}`);
line(`location_sort equals the GRCh37 start             : ${sameAs37}`);
line(`GRCh38 - GRCh37 offset  min ${offMin}  median ${offMedian}  max ${offMax}`);
line(`distinct GRCh38 - GRCh37 offsets over the sample  : ${offUnique.length}`);
line("  The browser submits location_sort, so with the hg19 assembly selected");
line("  the GRCh38 coordinate is sent to the GRCh37 endpoint.");

line("");
line("=".repeat(78));
line("E.4  Title parsing");
line("=".repeat(78));
line(`single nucleotide variants             : ${counts.single_nucleotide}`);
line(`deletions                             : ${counts.deletion}`);
line(`insertions / duplications              : ${counts.insertion}`);
line(`delins                                : ${counts.delins}`);
line(`other                                 : ${counts.other}`);
line(`classified as analyzable               : ${counts.analyzable}`);
line(`analyzable AND with a usable position  : ${counts.analyzable_with_usable_position}`);
line("derived request kind over all records : " + JSON.stringify(derivedKinds));

const out = {
  clinvar_records: records.length,
  clinvar_query: term,
  obj_type_counts: objTypes,
  review_status_counts: review,
  position_outcomes: posOutcomes,
  location_sort_is_grch38: sameAs38,
  location_sort_is_grch37: sameAs37,
  records_with_both_assemblies: both,
  grch38_minus_grch37_offset_min: offMin,
  grch38_minus_grch37_offset_median: offMedian,
  grch38_minus_grch37_offset_max: offMax,
  grch38_minus_grch37_distinct_offsets: offUnique.length,
  title_parse_counts: counts,
  derived_kind_counts: derivedKinds,
  zod_cases: zodResults.length,
  zod_conforming: zpass,
  sample_details: details.slice(0, 40),
};
fs.writeFileSync(
  path.join(REPO, "docs/analysis/e_clinvar_conformance.json"),
  JSON.stringify(out, null, 2),
);
line("");
line("wrote docs/analysis/e_clinvar_conformance.json");
