"use client";

import {
  type AnalysisResult,
  analyzeVariantWithAPI,
  fetchGeneSequence,
  inferDeletionLengthFromTitle,
  inferDelinsFromTitle,
  inferInsertedSequenceFromTitle,
  isDelinsClinvarVariant,
  isDeletionClinvarVariant,
  isInsertionClinvarVariant,
  type ClinvarVariant,
  type GeneBounds,
  type GeneFromSearch,
} from "~/utils/genome-api";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import React, {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import {
  getClassificationColorClasses,
  getNucleotideColorClass,
} from "~/utils/coloring-utils";
import { Button } from "./ui/button";
import { Zap } from "lucide-react";
import Link from "next/link";
import { useAuth } from "~/hooks/use-auth";

export interface VariantAnalysisHandle {
  focusAlternativeInput: () => void;
}

export type VariantType = "snv" | "deletion" | "insertion" | "delins";

interface VariantAnalysisProps {
  gene: GeneFromSearch;
  genomeId: string;
  chromosome: string;
  clinvarVariants: Array<ClinvarVariant>;
  referenceSequence: string | null;
  sequencePosition: number | null;
  geneBounds: GeneBounds | null;
  geneSequenceData?: string;
  geneSequenceRange?: { start: number; end: number } | null;
}

const VariantAnalysis = forwardRef<VariantAnalysisHandle, VariantAnalysisProps>(
  (
    {
      gene,
      genomeId,
      chromosome,
      clinvarVariants = [],
      referenceSequence,
      sequencePosition,
      geneBounds,
      geneSequenceData = "",
      geneSequenceRange = null,
    }: VariantAnalysisProps,
    ref,
  ) => {
    const [variantPosition, setVariantPosition] = useState<string>(
      geneBounds?.min?.toString() || "",
    );
    const [variantReference, setVariantReference] = useState("");
    const [variantAlternative, setVariantAlternative] = useState("");
    const [variantType, setVariantType] = useState<VariantType>("snv");
    const [deletionLength, setDeletionLength] = useState("1");
    const [insertedSequence, setInsertedSequence] = useState("");
    const [refPreview, setRefPreview] = useState<string | null>(null);
    const [isPreviewLoading, setIsPreviewLoading] = useState(false);
    const [variantResult, setVariantResult] = useState<AnalysisResult | null>(
      null,
    );
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [variantError, setVariantError] = useState<string | null>(null);
    const alternativeInputRef = useRef<HTMLInputElement>(null);
    const deletionLengthInputRef = useRef<HTMLInputElement>(null);
    const insertedSequenceInputRef = useRef<HTMLInputElement>(null);
    const { user, loading: authLoading } = useAuth();

    useImperativeHandle(ref, () => ({
      focusAlternativeInput: () => {
        if (variantType === "snv") {
          alternativeInputRef.current?.focus();
        } else if (variantType === "deletion") {
          deletionLengthInputRef.current?.focus();
        } else {
          insertedSequenceInputRef.current?.focus();
        }
      },
    }));

    useEffect(() => {
      if (sequencePosition && referenceSequence) {
        setVariantPosition(String(sequencePosition));
        setVariantReference(referenceSequence);
      }
    }, [sequencePosition, referenceSequence]);

    // Reference preview for indel types: prefer the already-loaded gene
    // sequence when it covers the range, otherwise fetch a small window.
    useEffect(() => {
      if (variantType === "snv") {
        setRefPreview(null);
        setIsPreviewLoading(false);
        return;
      }
      const pos = parseInt(variantPosition.replaceAll(",", ""));
      if (isNaN(pos) || pos <= 0) {
        setRefPreview(null);
        return;
      }
      let span = 1;
      if (variantType === "deletion" || variantType === "delins") {
        const len = parseInt(String(deletionLength).replaceAll(",", ""));
        if (isNaN(len) || len < 1 || len > 500) {
          setRefPreview(null);
          return;
        }
        span = len;
      }
      // Fast path: loaded gene sequence covers [pos, pos+span)
      if (
        geneSequenceData &&
        geneSequenceRange &&
        pos >= geneSequenceRange.start &&
        pos + span - 1 <= geneSequenceRange.end
      ) {
        const offset = pos - geneSequenceRange.start;
        setRefPreview(geneSequenceData.substring(offset, offset + span));
        setIsPreviewLoading(false);
        return;
      }
      let cancelled = false;
      setIsPreviewLoading(true);
      const timer = setTimeout(() => {
        void fetchGeneSequence(
          chromosome,
          pos,
          pos + span - 1,
          genomeId,
        ).then(({ sequence, error }) => {
          if (cancelled) return;
          setIsPreviewLoading(false);
          setRefPreview(!error && sequence ? sequence : null);
        });
      }, 400);
      return () => {
        cancelled = true;
        clearTimeout(timer);
      };
    }, [
      variantType,
      variantPosition,
      deletionLength,
      chromosome,
      genomeId,
      geneSequenceData,
      geneSequenceRange,
    ]);

    const parseDeletionLength = (raw: string): number | null => {
      const len = parseInt(String(raw).replaceAll(",", ""));
      if (isNaN(len) || len < 1 || len > 500) return null;
      return len;
    };

    const parseInsertedSequence = (raw: string): string | null => {
      const seq = String(raw ?? "")
        .toUpperCase()
        .replace(/\s+/g, "");
      if (!seq || seq.length > 500 || !/^[ATGC]+$/.test(seq)) return null;
      return seq;
    };

    const handlePositionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setVariantPosition(e.target.value);
      setVariantReference("");
    };

    const handleVariantSubmit = async (
      pos: string,
      args?: {
        type?: VariantType;
        alternative?: string;
        deletionLength?: string;
        insertedSequence?: string;
      },
    ) => {
      const type = args?.type ?? variantType;
      const alt = (args?.alternative ?? variantAlternative).toUpperCase();
      const delLenRaw = args?.deletionLength ?? deletionLength;
      const insRaw = args?.insertedSequence ?? insertedSequence;
      const position = parseInt(pos.replaceAll(",", ""));
      if (isNaN(position) || position <= 0) {
        setVariantError("Please enter a valid position number");
        return;
      }

      let apiPayload: Parameters<typeof analyzeVariantWithAPI>[0];
      if (type === "deletion") {
        const delLen = parseDeletionLength(delLenRaw);
        if (delLen == null) {
          setVariantError("Deletion length must be between 1 and 500 bp");
          return;
        }
        apiPayload = {
          position,
          variantType: "deletion",
          deletionLength: delLen,
          genomeId,
          chromosome,
        };
      } else if (type === "insertion") {
        const ins = parseInsertedSequence(insRaw);
        if (ins == null) {
          setVariantError(
            "Inserted sequence must be 1-500bp of A, C, G, T",
          );
          return;
        }
        apiPayload = {
          position,
          variantType: "insertion",
          insertedSequence: ins,
          genomeId,
          chromosome,
        };
      } else if (type === "delins") {
        const delLen = parseDeletionLength(delLenRaw);
        const ins = parseInsertedSequence(insRaw);
        if (delLen == null) {
          setVariantError("Deletion length must be between 1 and 500 bp");
          return;
        }
        if (ins == null) {
          setVariantError(
            "Inserted sequence must be 1-500bp of A, C, G, T",
          );
          return;
        }
        apiPayload = {
          position,
          variantType: "delins",
          deletionLength: delLen,
          insertedSequence: ins,
          genomeId,
          chromosome,
        };
      } else {
        const validNucleotides = /^[ATGC]$/;
        if (!validNucleotides.test(alt)) {
          setVariantError("Nucleotides must be A, C, G or T");
          return;
        }
        apiPayload = {
          position,
          variantType: "snv",
          alternative: alt,
          genomeId,
          chromosome,
        };
      }

      setIsAnalyzing(true);
      setVariantError(null);

      try {
        const data = await analyzeVariantWithAPI(apiPayload);
        setVariantResult(data);
      } catch (err) {
        console.error(err);
        setVariantError(
          err instanceof Error ? err.message : "Failed to analyze variant",
        );
      } finally {
        setIsAnalyzing(false);
      }
    };

    if (!authLoading && !user) {
      return (
        <Card className="gap-0 border-none bg-white py-0 shadow-sm">
          <CardHeader className="pt-4 pb-2">
            <CardTitle className="text-sm font-normal text-[#3c4f3d]/70">
              Variant Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="pb-4">
            <div className="rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4 text-xs text-[#3c4f3d]">
              Sign in to run Evo2 variant analysis.{" "}
              <Link href="/login" className="text-[#de8246] hover:underline">
                Sign in
              </Link>
            </div>
          </CardContent>
        </Card>
      );
    }

    return (
      <Card className="gap-0 border-none bg-white py-0 shadow-sm">
        <CardHeader className="pt-4 pb-2">
          <CardTitle className="text-sm font-normal text-[#3c4f3d]/70">
            Variant Analysis
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-4">
          <p className="mb-4 text-xs text-[#3c4f3d]/80">
            Predict the impact of genetic variants using the Evo2 deep learning
            model.
          </p>
          <div className="mb-3 flex w-fit flex-wrap rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-0.5 text-xs">
            {(
              [
                ["snv", "Substitution (SNV)"],
                ["deletion", "Deletion"],
                ["insertion", "Insertion"],
                ["delins", "Delins"],
              ] as [VariantType, string][]
            ).map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() => setVariantType(value)}
                className={`cursor-pointer rounded px-3 py-1.5 ${
                  variantType === value
                    ? "bg-white font-medium text-[#3c4f3d] shadow-sm"
                    : "text-[#3c4f3d]/60 hover:text-[#3c4f3d]"
                }`}
              >
                {label}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap items-end gap-4">
            <div>
              <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                {variantType === "snv"
                  ? "Position"
                  : variantType === "insertion"
                    ? "Anchor position"
                    : "Start position"}
              </label>
              <Input
                value={variantPosition}
                onChange={handlePositionChange}
                className="h-8 w-32 border-[#3c4f3d]/10 text-xs"
              />
            </div>
            {variantType === "snv" ? (
              <div>
                <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                  Alternative (variant)
                </label>
                <Input
                  ref={alternativeInputRef}
                  value={variantAlternative}
                  onChange={(e) =>
                    setVariantAlternative(e.target.value.toUpperCase())
                  }
                  className="h-8 w-32 border-[#3c4f3d]/10 text-xs"
                  placeholder="e.g., T"
                  maxLength={1}
                />
              </div>
            ) : variantType === "deletion" ? (
              <div>
                <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                  Deletion length (bp)
                </label>
                <Input
                  ref={deletionLengthInputRef}
                  value={deletionLength}
                  onChange={(e) =>
                    setDeletionLength(e.target.value.replace(/[^0-9]/g, ""))
                  }
                  className="h-8 w-32 border-[#3c4f3d]/10 text-xs"
                  placeholder="e.g., 3"
                  inputMode="numeric"
                />
              </div>
            ) : variantType === "insertion" ? (
              <div>
                <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                  Inserted sequence
                </label>
                <Input
                  ref={insertedSequenceInputRef}
                  value={insertedSequence}
                  onChange={(e) =>
                    setInsertedSequence(
                      e.target.value.toUpperCase().replace(/[^ATGC]/g, ""),
                    )
                  }
                  className="h-8 w-48 border-[#3c4f3d]/10 font-mono text-xs"
                  placeholder="e.g., ATG"
                  maxLength={500}
                />
              </div>
            ) : (
              <>
                <div>
                  <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                    Deletion length (bp)
                  </label>
                  <Input
                    ref={deletionLengthInputRef}
                    value={deletionLength}
                    onChange={(e) =>
                      setDeletionLength(e.target.value.replace(/[^0-9]/g, ""))
                    }
                    className="h-8 w-32 border-[#3c4f3d]/10 text-xs"
                    placeholder="e.g., 3"
                    inputMode="numeric"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-xs text-[#3c4f3d]/70">
                    Inserted sequence
                  </label>
                  <Input
                    ref={insertedSequenceInputRef}
                    value={insertedSequence}
                    onChange={(e) =>
                      setInsertedSequence(
                        e.target.value.toUpperCase().replace(/[^ATGC]/g, ""),
                      )
                    }
                    className="h-8 w-48 border-[#3c4f3d]/10 font-mono text-xs"
                    placeholder="e.g., ATG"
                    maxLength={500}
                  />
                </div>
              </>
            )}
            {variantType === "snv" && variantReference ? (
              <div className="mb-2 flex items-center gap-2 text-xs text-[#3c4f3d]">
                <span>Substitution</span>
                <span
                  className={`font-medium ${getNucleotideColorClass(variantReference)}`}
                >
                  {variantReference}
                </span>
                <span>→</span>
                <span
                  className={`font-medium ${getNucleotideColorClass(variantAlternative)}`}
                >
                  {variantAlternative ? variantAlternative : "?"}
                </span>
              </div>
            ) : variantType === "deletion" && variantReference ? (
              <div className="mb-2 flex items-center gap-2 text-xs text-[#3c4f3d]">
                <span>Deletion</span>
                <span
                  className={`font-medium ${getNucleotideColorClass(variantReference)}`}
                >
                  {variantReference}
                </span>
                <span>→</span>
                <span className="font-medium">del</span>
                <span className="text-[#3c4f3d]/60">
                  ({deletionLength || "?"} bp at {variantPosition || "?"})
                </span>
              </div>
            ) : variantType === "insertion" && variantReference ? (
              <div className="mb-2 flex items-center gap-2 text-xs text-[#3c4f3d]">
                <span>Insertion</span>
                <span
                  className={`font-medium ${getNucleotideColorClass(variantReference)}`}
                >
                  {variantReference}
                </span>
                <span>→</span>
                <span className="font-mono font-medium">
                  ins{insertedSequence ? insertedSequence : "?"}
                </span>
              </div>
            ) : variantType === "delins" ? (
              <div className="mb-2 flex items-center gap-2 text-xs text-[#3c4f3d]">
                <span>Delins</span>
                <span className="font-mono font-medium">
                  del {deletionLength || "?"}bp → {insertedSequence || "?"}
                </span>
                <span className="text-[#3c4f3d]/60">
                  at {variantPosition || "?"}
                </span>
              </div>
            ) : null}
            {variantType !== "snv" && (
              <div className="mb-2 w-full text-xs text-[#3c4f3d]/70">
                {isPreviewLoading ? (
                  <span>Loading reference preview…</span>
                ) : refPreview ? (
                  <span>
                    Reference{" "}
                    <span className="font-mono font-medium text-[#3c4f3d]">
                      {refPreview}
                    </span>{" "}
                    {variantType === "deletion" && "will be deleted"}
                    {variantType === "insertion" &&
                      `anchor ${(variantReference || refPreview.charAt(0) || "?").toUpperCase()} — insertion occurs after this base`}
                    {variantType === "delins" &&
                      `will be replaced with ${(insertedSequence || "?").toUpperCase()}`}
                  </span>
                ) : (
                  variantPosition &&
                  (variantType === "deletion" || variantType === "delins") && (
                    <span className="text-[#3c4f3d]/50">
                      Enter a valid position and length to preview the deleted
                      sequence.
                    </span>
                  )
                )}
              </div>
            )}
            <Button
              disabled={
                isAnalyzing ||
                !variantPosition ||
                (variantType === "snv"
                  ? !variantAlternative
                  : variantType === "deletion"
                    ? !deletionLength
                    : variantType === "insertion"
                      ? !insertedSequence
                      : !deletionLength || !insertedSequence)
              }
              className="h-8 cursor-pointer bg-[#3c4f3d] text-xs text-white hover:bg-[#3c4f3d]/90 transition-all duration-200 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
              onClick={() => {
                void handleVariantSubmit(variantPosition.replaceAll(",", ""));
              }}
            >
              {isAnalyzing ? (
                <>
                  <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent align-middle"></span>
                  Analyzing...
                </>
              ) : (
                "Analyze variant"
              )}
            </Button>
          </div>

          {variantPosition &&
            clinvarVariants
              .filter(
                (variant) => {
                  const loc = parseInt(
                    variant?.location?.replaceAll(",", "") ?? "",
                  );
                  const pos = parseInt(variantPosition.replaceAll(",", ""));
                  if (isNaN(loc) || isNaN(pos) || loc !== pos) return false;
                  const vt = variant?.variation_type?.toLowerCase() ?? "";
                  return (
                    vt.includes("single nucleotide") ||
                    vt.includes("deletion") ||
                    vt.includes("insertion") ||
                    vt.includes("duplication") ||
                    isDeletionClinvarVariant(variant) ||
                    isInsertionClinvarVariant(variant) ||
                    isDelinsClinvarVariant(variant)
                  );
                },
              )
              .map((matchedVariant) => {
                if (isDelinsClinvarVariant(matchedVariant)) {
                  const parsed = inferDelinsFromTitle(matchedVariant.title);
                  if (!parsed) return null;
                  return (
                    <div
                      key={matchedVariant.clinvar_id}
                      className="mt-4 rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4"
                    >
                      <div className="mb-3 flex items-center justify-between">
                        <h4 className="text-sm font-medium text-[#3c4f3d]">
                          Known Variant Detected
                        </h4>
                        <span className="text-xs text-[#3c4f3d]/70">
                          Position: {matchedVariant.location}
                        </span>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <div className="mb-1 text-xs font-medium text-[#3c4f3d]/70">
                            Variant Details
                          </div>
                          <div className="text-sm">{matchedVariant.title}</div>
                          <div className="mt-2 text-sm">
                            {gene?.symbol} {variantPosition}{" "}
                            <span className="font-mono">
                              del ({parsed.deletionLength}bp) →{" "}
                              {parsed.inserted}
                            </span>
                          </div>
                          <div className="mt-2 text-xs text-[#3c4f3d]/70">
                            ClinVar classification
                            <span
                              className={`ml-1 rounded-sm px-2 py-0.5 ${getClassificationColorClasses(matchedVariant.classification)}`}
                            >
                              {matchedVariant.classification || "Unknown"}
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center justify-end">
                          <Button
                            disabled={isAnalyzing}
                            variant="outline"
                            size="sm"
                            className="h-7 cursor-pointer border-[#3c4f3d]/20 bg-[#e9eeea] text-xs text-[#3c4f3d] hover:bg-[#3c4f3d]/10 transition-all duration-150 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
                            onClick={() => {
                              setVariantType("delins");
                              setDeletionLength(String(parsed.deletionLength));
                              setInsertedSequence(parsed.inserted);
                              void handleVariantSubmit(
                                variantPosition.replaceAll(",", ""),
                                {
                                  type: "delins",
                                  deletionLength: String(parsed.deletionLength),
                                  insertedSequence: parsed.inserted,
                                },
                              );
                            }}
                          >
                            {isAnalyzing ? (
                              <>
                                <span className="mr-1 inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent align-middle"></span>
                                Analyzing...
                              </>
                            ) : (
                              <>
                                <Zap className="mr-1 inline-block h-3 w-3" />
                                Analyze this Delins
                              </>
                            )}
                          </Button>
                        </div>
                      </div>
                    </div>
                  );
                }
                if (
                  isInsertionClinvarVariant(matchedVariant) &&
                  !isDeletionClinvarVariant(matchedVariant)
                ) {
                  const ins = inferInsertedSequenceFromTitle(
                    matchedVariant.title,
                  );
                  if (!ins) return null;
                  return (
                    <div
                      key={matchedVariant.clinvar_id}
                      className="mt-4 rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4"
                    >
                      <div className="mb-3 flex items-center justify-between">
                        <h4 className="text-sm font-medium text-[#3c4f3d]">
                          Known Variant Detected
                        </h4>
                        <span className="text-xs text-[#3c4f3d]/70">
                          Position: {matchedVariant.location}
                        </span>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <div className="mb-1 text-xs font-medium text-[#3c4f3d]/70">
                            Variant Details
                          </div>
                          <div className="text-sm">{matchedVariant.title}</div>
                          <div className="mt-2 text-sm">
                            {gene?.symbol} {variantPosition}{" "}
                            <span className="font-mono">ins{ins}</span>
                          </div>
                          <div className="mt-2 text-xs text-[#3c4f3d]/70">
                            ClinVar classification
                            <span
                              className={`ml-1 rounded-sm px-2 py-0.5 ${getClassificationColorClasses(matchedVariant.classification)}`}
                            >
                              {matchedVariant.classification || "Unknown"}
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center justify-end">
                          <Button
                            disabled={isAnalyzing}
                            variant="outline"
                            size="sm"
                            className="h-7 cursor-pointer border-[#3c4f3d]/20 bg-[#e9eeea] text-xs text-[#3c4f3d] hover:bg-[#3c4f3d]/10 transition-all duration-150 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
                            onClick={() => {
                              setVariantType("insertion");
                              setInsertedSequence(ins);
                              void handleVariantSubmit(
                                variantPosition.replaceAll(",", ""),
                                {
                                  type: "insertion",
                                  insertedSequence: ins,
                                },
                              );
                            }}
                          >
                            {isAnalyzing ? (
                              <>
                                <span className="mr-1 inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent align-middle"></span>
                                Analyzing...
                              </>
                            ) : (
                              <>
                                <Zap className="mr-1 inline-block h-3 w-3" />
                                Analyze this Insertion
                              </>
                            )}
                          </Button>
                        </div>
                      </div>
                    </div>
                  );
                }
                const isDel = isDeletionClinvarVariant(matchedVariant);
                if (isDel) {
                  const delLen = inferDeletionLengthFromTitle(
                    matchedVariant.title,
                  );
                  return (
                    <div
                      key={matchedVariant.clinvar_id}
                      className="mt-4 rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4"
                    >
                      <div className="mb-3 flex items-center justify-between">
                        <h4 className="text-sm font-medium text-[#3c4f3d]">
                          Known Variant Detected
                        </h4>
                        <span className="text-xs text-[#3c4f3d]/70">
                          Position: {matchedVariant.location}
                        </span>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <div className="mb-1 text-xs font-medium text-[#3c4f3d]/70">
                            Variant Details
                          </div>
                          <div className="text-sm">{matchedVariant.title}</div>
                          <div className="mt-2 text-sm">
                            {gene?.symbol} {variantPosition}{" "}
                            <span className="font-mono">
                              del ({delLen}bp)
                            </span>
                          </div>
                          <div className="mt-2 text-xs text-[#3c4f3d]/70">
                            ClinVar classification
                            <span
                              className={`ml-1 rounded-sm px-2 py-0.5 ${getClassificationColorClasses(matchedVariant.classification)}`}
                            >
                              {matchedVariant.classification || "Unknown"}
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center justify-end">
                          <Button
                            disabled={isAnalyzing}
                            variant="outline"
                            size="sm"
                            className="h-7 cursor-pointer border-[#3c4f3d]/20 bg-[#e9eeea] text-xs text-[#3c4f3d] hover:bg-[#3c4f3d]/10 transition-all duration-150 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
                            onClick={() => {
                              setVariantType("deletion");
                              setDeletionLength(String(delLen));
                              void handleVariantSubmit(
                                variantPosition.replaceAll(",", ""),
                                {
                                  type: "deletion",
                                  deletionLength: String(delLen),
                                },
                              );
                            }}
                          >
                            {isAnalyzing ? (
                              <>
                                <span className="mr-1 inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent align-middle"></span>
                                Analyzing...
                              </>
                            ) : (
                              <>
                                <Zap className="mr-1 inline-block h-3 w-3" />
                                Analyze this Deletion
                              </>
                            )}
                          </Button>
                        </div>
                      </div>
                    </div>
                  );
                }

                const refAltMatch = matchedVariant.title.match(/(\w)>(\w)/);

                let ref = null;
                let alt = null;
                if (refAltMatch && refAltMatch.length === 3) {
                  ref = refAltMatch[1];
                  alt = refAltMatch[2];
                }

                if (!ref || !alt) return null;

                return (
                  <div
                    key={matchedVariant.clinvar_id}
                    className="mt-4 rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4"
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <h4 className="text-sm font-medium text-[#3c4f3d]">
                        Known Variant Detected
                      </h4>
                      <span className="text-xs text-[#3c4f3d]/70">
                        Position: {matchedVariant.location}
                      </span>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <div className="mb-1 text-xs font-medium text-[#3c4f3d]/70">
                          Variant Details
                        </div>
                        <div className="text-sm">{matchedVariant.title}</div>
                        <div className="mt-2 text-sm">
                          {gene?.symbol} {variantPosition}{" "}
                          <span className="font-mono">
                            <span className={getNucleotideColorClass(ref)}>
                              {ref}
                            </span>
                            <span>{">"}</span>
                            <span className={getNucleotideColorClass(alt)}>
                              {alt}
                            </span>
                          </span>
                        </div>
                        <div className="mt-2 text-xs text-[#3c4f3d]/70">
                          ClinVar classification
                          <span
                            className={`ml-1 rounded-sm px-2 py-0.5 ${getClassificationColorClasses(matchedVariant.classification)}`}
                          >
                            {matchedVariant.classification || "Unknown"}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center justify-end">
                        <Button
                          disabled={isAnalyzing}
                          variant="outline"
                          size="sm"
                          className="h-7 cursor-pointer border-[#3c4f3d]/20 bg-[#e9eeea] text-xs text-[#3c4f3d] hover:bg-[#3c4f3d]/10"
                          onClick={() => {
                            setVariantType("snv");
                            setVariantAlternative(alt);
                            void handleVariantSubmit(
                              variantPosition.replaceAll(",", ""),
                              { type: "snv", alternative: alt },
                            );
                          }}
                        >
                          {isAnalyzing ? (
                            <>
                              <span className="mr-1 inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent align-middle"></span>
                              Analyzing...
                            </>
                          ) : (
                            <>
                              <Zap className="mr-1 inline-block h-3 w-3" />
                              Analyze this Variant
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  </div>
                );
              })[0]}
          {variantError && (
            <div className="mt-4 rounded-md bg-red-50 p-3 text-xs text-red-600">
              {variantError}
            </div>
          )}
          {variantResult && (
            <div className="mt-6 rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4">
              <h4 className="mb-3 text-sm font-medium text-[#3c4f3d]">
                Analysis Result
              </h4>
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <div className="mb-2">
                    <div className="text-xs font-medium text-[#3c4f3d]/70">
                      Variant
                    </div>
                    <div className="text-sm">
                      {gene?.symbol} {variantResult.position}{" "}
                      <span className="font-mono">
                        {variantResult.variant_type === "deletion" ? (
                          <>
                            {variantResult.reference}
                            {"→del"}
                            {(variantResult.deletion_length ??
                              variantResult.reference?.length) > 1 && (
                              <span className="text-[#3c4f3d]/60">
                                {" "}
                                (
                                {variantResult.deletion_length ??
                                  variantResult.reference?.length}
                                bp)
                              </span>
                            )}
                          </>
                        ) : variantResult.variant_type === "insertion" ? (
                          <>
                            {variantResult.reference}
                            {"→ins"}
                            {variantResult.inserted_sequence ??
                              variantResult.alternative}
                          </>
                        ) : variantResult.variant_type === "delins" ? (
                          <>
                            {variantResult.reference}
                            {"→"}
                            {variantResult.inserted_sequence ??
                              variantResult.alternative}
                            <span className="text-[#3c4f3d]/60">
                              {" "}
                              (del{" "}
                              {variantResult.deletion_length ??
                                variantResult.reference?.length}
                              bp)
                            </span>
                          </>
                        ) : (
                          <>
                            {variantResult.reference}
                            {">"}
                            {variantResult.alternative}
                          </>
                        )}
                      </span>
                    </div>
                    {variantResult.provisional_prediction && (
                      <div className="mt-2 inline-block rounded-md bg-yellow-50 px-2 py-1 text-xs text-yellow-700">
                        Provisional classification — thresholds calibrated on
                        SNVs, indel calibration pending
                      </div>
                    )}
                  </div>
                  <div>
                    <div className="text-xs font-medium text-[#3c4f3d]/70">
                      Delta likelihood score
                    </div>
                    <div className="text-sm">
                      {variantResult.delta_score.toFixed(6)}
                    </div>
                    <div className="text-xs text-[#3c4f3d]/60">
                      Negative score indicates loss of function
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-xs font-medium text-[#3c4f3d]/70">
                    Prediction
                  </div>
                  <div
                    className={`inline-block rounded-lg px-3 py-1 text-xs ${getClassificationColorClasses(variantResult.prediction)}`}
                  >
                    {variantResult.prediction}
                  </div>
                  <div className="mt-3">
                    <div className="text-xs font-medium text-[#3c4f3d]/70">
                      Confidence
                    </div>
                    <div className="mt-1 h-2 w-full rounded-full bg-[#e9eeea]">
                      <div
                        className={`h-2 rounded-full ${variantResult.prediction.includes("pathogenic") ? "bg-red-600" : "bg-green-600"}`}
                        style={{
                          width: `${Math.min(100, variantResult.classification_confidence * 100)}%`,
                        }}
                      ></div>
                    </div>
                    <div className="mt-1 text-right text-xs text-[#3c4f3d]/60">
                      {Math.round(
                        variantResult.classification_confidence * 100,
                      )}
                      %
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    );
  },
);
VariantAnalysis.displayName = "VariantAnalysis";

export default VariantAnalysis;
