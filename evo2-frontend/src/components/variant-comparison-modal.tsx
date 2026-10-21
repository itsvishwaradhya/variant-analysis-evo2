import type { ClinvarVariant } from "~/utils/genome-api";
import { inferDeletionLengthFromTitle } from "~/utils/genome-api";
import { useEffect } from "react";
import { Button } from "./ui/button";
import { Check, ExternalLink, Shield, X } from "lucide-react";
import {
  getClassificationColorClasses,
  getNucleotideColorClass,
} from "~/utils/coloring-utils";

export function VariantComparisonModal({
  comparisonVariant,
  onClose,
}: {
  comparisonVariant: ClinvarVariant | null;
  onClose: () => void;
}) {
  const isOpen = Boolean(comparisonVariant?.evo2Result);

  useEffect(() => {
    if (!isOpen) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Variant Analysis Comparison"
      className="fixed inset-0 z-50 flex items-center justify-center overscroll-contain bg-black/50 p-4"
    >
      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto overscroll-contain rounded-lg bg-white">
        {/* Modal header */}
        <div className="border-b border-[#3c4f3d]/10 p-5">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-[#3c4f3d]">
              Variant Analysis Comparison
            </h3>
            <button
              type="button"
              aria-label="Close comparison"
              onClick={onClose}
              className="h-7 w-7 cursor-pointer rounded-md p-0 text-[#3c4f3d]/70 hover:bg-[#e9eeea]/70 hover:text-[#3c4f3d] outline-none focus-visible:ring-2 focus-visible:ring-[#de8246]/50 transition-[background-color,color] duration-150 ease-[var(--ease-micro)]"
            >
              <X className="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
        </div>

        {/* Modal content */}
        <div className="p-5">
          {comparisonVariant && comparisonVariant.evo2Result && (
            <div className="space-y-6">
              <div className="rounded-md border border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4">
                <h4 className="mb-3 text-sm font-medium text-[#3c4f3d]">
                  Variant Information
                </h4>
                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <div className="space-y-2">
                      <div className="flex">
                        <span className="w-28 text-xs text-[#3c4f3d]/70">
                          Position:
                        </span>
                        <span className="text-xs">
                          {comparisonVariant.location}
                        </span>
                      </div>
                      <div className="flex">
                        <span className="w-28 text-xs text-[#3c4f3d]/70">
                          Type:
                        </span>
                        <span className="text-xs">
                          {comparisonVariant.variation_type}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div className="space-y-2">
                      <div className="flex">
                        <span className="w-28 text-xs text-[#3c4f3d]/70">
                          Variant:
                        </span>
                        <span className="font-mono text-xs">
                          {(() => {
                            const evo2 = comparisonVariant.evo2Result;
                            if (evo2?.variant_type === "deletion") {
                              const ref = evo2.reference ?? "";
                              const len =
                                evo2.deletion_length ?? ref.length ?? 1;
                              return (
                                <>
                                  <span>{ref}</span>
                                  <span>{"→del"}</span>
                                  {len > 1 && (
                                    <span className="text-[#3c4f3d]/60">
                                      {" "}
                                      ({len}bp)
                                    </span>
                                  )}
                                </>
                              );
                            }
                            if (evo2?.variant_type === "insertion") {
                              return (
                                <>
                                  <span>{evo2.reference ?? ""}</span>
                                  <span>{"→ins"}</span>
                                  <span>
                                    {evo2.inserted_sequence ??
                                      evo2.alternative ??
                                      ""}
                                  </span>
                                </>
                              );
                            }
                            if (evo2?.variant_type === "delins") {
                              return (
                                <>
                                  <span>{evo2.reference ?? ""}</span>
                                  <span>{"→"}</span>
                                  <span>
                                    {evo2.inserted_sequence ??
                                      evo2.alternative ??
                                      ""}
                                  </span>
                                  <span className="text-[#3c4f3d]/60">
                                    {" "}
                                    (del{" "}
                                    {evo2.deletion_length ??
                                      (evo2.reference?.length || "?")}
                                    bp)
                                  </span>
                                </>
                              );
                            }
                            const match =
                              comparisonVariant.title.match(/(\w)>(\w)/);
                            if (match && match.length === 3) {
                              const [_, ref, alt] = match;
                              return (
                                <>
                                  <span
                                    className={getNucleotideColorClass(ref!)}
                                  >
                                    {ref}
                                  </span>
                                  <span>{">"}</span>
                                  <span
                                    className={getNucleotideColorClass(alt!)}
                                  >
                                    {alt}
                                  </span>
                                </>
                              );
                            }
                            if (/delins/i.test(comparisonVariant.title)) {
                              return (
                                <>
                                  <span>{comparisonVariant.title}</span>
                                  <span className="text-[#3c4f3d]/60">
                                    {" "}
                                    (delins)
                                  </span>
                                </>
                              );
                            }
                            if (/del/i.test(comparisonVariant.title)) {
                              const len = inferDeletionLengthFromTitle(
                                comparisonVariant.title,
                              );
                              return (
                                <>
                                  <span>{comparisonVariant.title}</span>
                                  <span className="text-[#3c4f3d]/60">
                                    {" "}
                                    (del{len > 1 ? ` ${len}bp` : ""})
                                  </span>
                                </>
                              );
                            }
                            return comparisonVariant.title;
                          })()}
                        </span>
                      </div>
                      <div className="flex items-center">
                        <span className="w-28 text-xs text-[#3c4f3d]/70">
                          ClinVar ID:
                        </span>
                        <a
                          href={`https://www.ncbi.nlm.nih.gov/clinvar/variation/${comparisonVariant.clinvar_id}`}
                          className="text-xs text-[#de8246] hover:underline"
                          target="_blank"
                        >
                          {comparisonVariant.clinvar_id}
                        </a>
                        <ExternalLink className="ml-1 inline-block h-3 w-3 text-[#de8246]" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Variant results */}
              <div>
                <h4 className="mb-3 text-sm font-medium text-[#3c4f3d]">
                  Analysis Comparison
                </h4>
                <div className="rounded-md border border-[#3c4f3d]/10 bg-white p-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    {/* ClinVar Assesment */}
                    <div className="rounded-md bg-[#e9eeea]/50 p-4">
                      <h5 className="mb-2 flex items-center gap-2 text-xs font-medium text-[#3c4f3d]">
                        <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#3c4f3d]/10">
                          <span className="h-3 w-3 rounded-full bg-[#3c4f3d]"></span>
                        </span>
                        ClinVar Assessment
                      </h5>
                      <div className="mt-2">
                        <div
                          className={`w-fit rounded-md px-2 py-1 text-xs font-normal ${getClassificationColorClasses(comparisonVariant.classification)}`}
                        >
                          {comparisonVariant.classification ||
                            "Unknown significance"}
                        </div>
                      </div>
                    </div>

                    {/* Evo2 Prediction */}
                    <div className="rounded-md bg-[#e9eeea]/50 p-4">
                      <h5 className="mb-2 flex items-center gap-2 text-xs font-medium text-[#3c4f3d]">
                        <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#3c4f3d]/10">
                          <span className="h-3 w-3 rounded-full bg-[#de8246]"></span>
                        </span>
                        Evo2 Prediction
                      </h5>
                      <div className="mt-2">
                        <div
                          className={`flex w-fit items-center gap-1 rounded-md px-2 py-1 text-xs font-normal ${getClassificationColorClasses(comparisonVariant.evo2Result.prediction)}`}
                        >
                          <Shield className="h-3 w-3" />
                          {comparisonVariant.evo2Result.prediction}
                        </div>
                        {comparisonVariant.evo2Result.provisional_prediction && (
                          <div className="mt-2 w-fit rounded-md bg-yellow-50 px-2 py-1 text-xs text-yellow-700">
                            Provisional — indel thresholds pending calibration
                          </div>
                        )}
                      </div>
                      {/* Delta score */}
                      <div className="mt-3">
                        <div className="mb-1 text-xs text-[#3c4f3d]/70">
                          Delta Likelihood Score:
                        </div>
                        <div className="text-sm font-medium">
                          {comparisonVariant.evo2Result.delta_score.toFixed(6)}
                        </div>
                        <div className="text-xs text-[#3c4f3d]/60">
                          {comparisonVariant.evo2Result.delta_score < 0
                            ? "Negative score indicates loss of function"
                            : "Positive score indicated gain/neutral function"}
                        </div>
                      </div>
                      {/* Confidence bar */}
                      <div className="mt-3">
                        <div className="mb-1 text-xs text-[#3c4f3d]/70">
                          Confidence:
                        </div>
                        <div className="mt-1 h-2 w-full rounded-full bg-[#e9eeea]/80">
                          <div
                            className={`h-2 rounded-full ${comparisonVariant.evo2Result.prediction.includes("pathogenic") ? "bg-red-600" : "bg-green-600"}`}
                            style={{
                              width: `${Math.min(100, comparisonVariant.evo2Result.classification_confidence * 100)}%`,
                            }}
                          ></div>
                        </div>
                        <div className="mt-1 text-right text-xs text-[#3c4f3d]/60">
                          {Math.round(
                            comparisonVariant.evo2Result
                              .classification_confidence * 100,
                          )}
                          %
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Assesment Agreement */}
                  <div className="mt-4 rounded-md bg-[#e9eeea]/20 p-3 text-xs leading-relaxed">
                    <div className="flex items-center gap-2">
                      <span
                        className={`flex h-5 w-5 items-center justify-center rounded-full ${comparisonVariant.classification.toLowerCase() === comparisonVariant.evo2Result.prediction.toLowerCase() ? "bg-green-100" : "bg-yellow-100"}`}
                      >
                        {comparisonVariant.classification.toLowerCase() ===
                        comparisonVariant.evo2Result.prediction.toLowerCase() ? (
                          <Check className="h-3 w-3 text-green-600" />
                        ) : (
                          <span className="flex h-3 w-3 items-center justify-center text-yellow-600">
                            <p>!</p>
                          </span>
                        )}
                      </span>
                      <span className="font-medium text-[#3c4f3d]">
                        {comparisonVariant.classification.toLowerCase() ===
                        comparisonVariant.evo2Result.prediction.toLowerCase()
                          ? "Evo2 prediction agrees with ClinVar classification"
                          : "Evo2 prediction differs from ClinVar classification"}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal footer */}
        <div className="flex justify-end border-t border-[#3c4f3d]/10 bg-[#e9eeea]/30 p-4">
          <Button
            variant="outline"
            onClick={onClose}
            className="cursor-pointer border-[#3c4f3d]/10 bg-white text-[#3c4f3d] hover:bg-[#e9eeea]/70"
          >
            Close
          </Button>
        </div>
      </div>
    </div>
  );
}
