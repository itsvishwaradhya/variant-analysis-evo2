"use client";

import { Clapperboard, Search, SearchCodeIcon } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import GeneViewer from "~/components/gene-viewer";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Input } from "~/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import {
  type ChromosomeFromSeach,
  type GeneFromSearch,
  type GenomeAssemblyFromSearch,
  getAvailableGenomes,
  getGenomeChromosomes,
  searchGenes,
} from "~/utils/genome-api";
import { useAuth } from "~/hooks/use-auth";

type Mode = "browse" | "search";

export default function HomePage() {
  const [genomes, setGenomes] = useState<GenomeAssemblyFromSearch[]>([]);
  const [selectedGenome, setSelectedGenome] = useState<string>("hg38");
  const [chromosomes, setChromosomes] = useState<ChromosomeFromSeach[]>([]);
  const [selectedChromosome, setSelectedChromosome] = useState<string>("chr1");
  const [selectedGene, setSelectedGene] = useState<GeneFromSearch | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<GeneFromSearch[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<Mode>("search");
  const { user, loading: authLoading, logout } = useAuth();

  useEffect(() => {
    const fetchGenomes = async () => {
      try {
        setIsLoading(true);
        const data = await getAvailableGenomes();
        if (data.genomes && data.genomes["Human"]) {
          setGenomes(data.genomes["Human"]);
        }
      } catch (err) {
        setError("Failed to load genome data");
      } finally {
        setIsLoading(false);
      }
    };
    fetchGenomes();
  }, []);

  useEffect(() => {
    const fetchChromosomes = async () => {
      try {
        setIsLoading(true);
        const data = await getGenomeChromosomes(selectedGenome);
        setChromosomes(data.chromosomes);
        console.log(data.chromosomes);
        if (data.chromosomes.length > 0) {
          setSelectedChromosome(data.chromosomes[0]!.name);
        }
      } catch (err) {
        setError("Failed to load chromosome data");
      } finally {
        setIsLoading(false);
      }
    };
    fetchChromosomes();
  }, [selectedGenome]);

  const performGeneSearch = async (
    query: string,
    genome: string,
    filterFn?: (gene: GeneFromSearch) => boolean,
  ) => {
    try {
      setIsLoading(true);
      const data = await searchGenes(query, genome);
      const results = filterFn ? data.results.filter(filterFn) : data.results;

      setSearchResults(results);
    } catch (err) {
      setError("Faield to search genes");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!selectedChromosome || mode !== "browse") return;
    performGeneSearch(
      selectedChromosome,
      selectedGenome,
      (gene: GeneFromSearch) => gene.chrom === selectedChromosome,
    );
  }, [selectedChromosome, selectedGenome, mode]);

  const handleGenomeChange = (value: string) => {
    setSelectedGenome(value);
    setSearchResults([]);
    setSelectedGene(null);
  };

  const switchMode = (newMode: Mode) => {
    if (newMode === mode) return;

    setSearchResults([]);
    setSelectedGene(null);
    setError(null);

    if (newMode === "browse" && selectedChromosome) {
      performGeneSearch(
        selectedChromosome,
        selectedGenome,
        (gene: GeneFromSearch) => gene.chrom === selectedChromosome,
      );
    }

    setMode(newMode);
  };

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!searchQuery.trim()) return;

    performGeneSearch(searchQuery, selectedGenome);
  };

  const loadBRCA1Example = () => {
    setMode("search");
    setSearchQuery("BRCA1");
    performGeneSearch("BRCA1", selectedGenome);
  };

  return (
    <div className="min-h-screen bg-[#e9eeea] relative dither-overlay">
      <nav className="fixed top-4 left-1/2 z-50 -translate-x-1/2 rounded-2xl bg-white/70 backdrop-blur-xl border border-white/20 shadow-[0_8px_32px_rgba(60,79,61,0.08)] px-6 py-3 flex items-center gap-6 transition-[transform,box-shadow] duration-300 ease-[var(--ease-micro)] hover:shadow-[0_12px_40px_rgba(60,79,61,0.15)] hover:-translate-y-0.5 hover:scale-[1.01] active:scale-[0.99]" style={{ animation: 'fadeSlideDown 0.7s var(--ease-micro)' }}>
        {/* Logo */}
        <Link href="/" className="group flex items-center gap-2.5 transition-transform duration-300 ease-[var(--ease-micro)] hover:scale-105 active:scale-95">
          <div className="relative flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-br from-[#de8246] to-[#b86e3c] shadow-sm overflow-hidden">
            <div className="absolute inset-0 rounded-full bg-gradient-to-t from-white/15 to-transparent"></div>
            <span className="relative text-white font-bold text-sm tracking-tight">E2</span>
          </div>
          <div className="flex flex-col leading-none">
            <span className="text-[13px] font-semibold text-[#3c4f3d] tracking-wide">EVO</span>
            <span className="text-[10px] text-[#de8246] font-medium tracking-widest">VARIANT</span>
          </div>
        </Link>

        {/* Divider */}
        <div className="h-5 w-px bg-[#3c4f3d]/10 rounded-full"></div>

        {/* Auth */}
        <div className="flex items-center">
          {authLoading ? (
            <div className="w-20 h-7 rounded-full bg-[#e9eeea] animate-pulse"></div>
          ) : user ? (
            <div className="flex items-center gap-3">
              <span className="text-[11px] text-[#3c4f3d]/60 font-medium hidden sm:inline truncate max-w-[180px]">{user.email}</span>
              <button
                onClick={() => void logout()}
                className="text-[11px] px-3.5 py-1.5 rounded-full bg-[#e9eeea] text-[#3c4f3d]/80 border border-[#3c4f3d]/10 hover:bg-[#3c4f3d]/10 hover:text-[#3c4f3d] hover:border-[#3c4f3d]/20 focus-visible:ring-2 focus-visible:ring-[#de8246]/50 outline-none transition-[background-color,border-color,color,transform] duration-200 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="text-[11px] px-3.5 py-1.5 rounded-full bg-[#3c4f3d] text-white font-medium shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-[#de8246]/60 focus-visible:ring-offset-2 focus-visible:ring-offset-[#e9eeea] transition-[transform,box-shadow] duration-200 ease-[var(--ease-micro)] hover:shadow-md hover:-translate-y-px hover:scale-[1.04] active:translate-y-0 active:scale-[0.98]"
            >
              Sign in
            </Link>
          )}
        </div>
      </nav>

      <main className="container mx-auto px-6 pt-24 pb-6 relative">
        {selectedGene ? (
          <div className="animate-[blurReveal_0.7s_ease-[var(--ease-micro)]]">
            <GeneViewer
              gene={selectedGene}
              genomeId={selectedGenome}
              onClose={() => setSelectedGene(null)}
            />
          </div>
        ) : (
          <>
            <Card className="mb-6 gap-0 border-none bg-white py-0 shadow-sm animate-[blurReveal_0.8s_ease-[var(--ease-micro)]]">
              <CardHeader className="pt-4 pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm font-normal text-[#3c4f3d]/70">
                    Genome Assembly
                  </CardTitle>
                  <div className="text-xs text-[#3c4f3d]/60">
                    Organism: <span className="font-medium">Human</span>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pb-4">
                <Select
                  value={selectedGenome}
                  onValueChange={handleGenomeChange}
                  disabled={isLoading}
                >
                  <SelectTrigger className="h-9 w-full border-[#3c4f3d]/10">
                    <SelectValue placeholder="Select genome assembly" />
                  </SelectTrigger>
                  <SelectContent>
                    {genomes.map((genome) => (
                      <SelectItem key={genome.id} value={genome.id}>
                        {genome.id} - {genome.name}
                        {genome.active ? " (active)" : ""}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {selectedGenome && (
                  <p className="mt-2 text-xs text-[#3c4f3d]/60">
                    {
                      genomes.find((genome) => genome.id === selectedGenome)
                        ?.sourceName
                    }
                  </p>
                )}
              </CardContent>
            </Card>

            <Card className="mt-6 gap-0 border-none bg-white py-0 shadow-sm animate-[blurReveal_1s_ease-[var(--ease-micro)]]">
              <CardHeader className="pt-4 pb-2">
                <CardTitle className="text-sm font-normal text-[#3c4f3d]/70">
                  Browse
                </CardTitle>
              </CardHeader>
              <CardContent className="pb-4">
                <Tabs
                  value={mode}
                  onValueChange={(value) => switchMode(value as Mode)}
                >
                  <TabsList className="mb-4 bg-[#e9eeea]">
                    <TabsTrigger
                      className="data-[state=active]:bg-white data-[state=active]:text-[#3c4f3d]"
                      value="search"
                    >
                      Search Genes
                    </TabsTrigger>
                    <TabsTrigger
                      className="data-[state=active]:bg-white data-[state=active]:text-[#3c4f3d]"
                      value="browse"
                    >
                      Browse Chromosomes
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="search" className="mt-0">
                    <div className="space-y-4">
                      <form
                        onSubmit={handleSearch}
                        className="flex flex-col gap-3 sm:flex-row"
                      >
                        <div className="relative flex-1">
                          <Input
                            type="text"
                            name="gene-search"
                            aria-label="Gene symbol or name"
                            placeholder="e.g. BRCA1…"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="h-9 border-[#3c4f3d]/10 pr-10"
                          />
                          <Button
                            type="submit"
                            className="absolute top-0 right-0 h-full cursor-pointer rounded-l-none bg-[#3c4f3d] text-white hover:bg-[#3c4f3d]/90 transition-[background-color,transform] duration-200 ease-[var(--ease-micro)] hover:-translate-y-px active:translate-y-0"
                            size="icon"
                            disabled={isLoading || !searchQuery.trim()}
                          >
                            <Search className="h-4 w-4" />
                            <span className="sr-only">Search</span>
                          </Button>
                        </div>
                      </form>
                      <Button
                        variant="link"
                        className="h-auto cursor-pointer p-0 text-[#de8246] hover:text-[#de8246]/80 hover:-translate-y-px transition-[color,transform] duration-150 ease-[var(--ease-micro)]"
                        onClick={loadBRCA1Example}
                      >
                        Try BRCA1 example
                      </Button>
                    </div>
                  </TabsContent>

                  <TabsContent value="browse" className="mt-0">
                    <div className="max-h-[150px] overflow-y-auto pr-1">
                      <div className="flex flex-wrap gap-2">
                        {chromosomes.map((chrom) => (
                          <Button
                            key={chrom.name}
                            variant="outline"
                            size="sm"
                            className={`h-8 cursor-pointer border-[#3c4f3d]/10 hover:bg-[#e9eeea] hover:text-[#3c4f3d] hover:-translate-y-px transition-[background-color,color,border-color,transform] duration-150 ease-[var(--ease-micro)] ${selectedChromosome === chrom.name ? "text-[#3c4f3d] bg-[#e9eeea]" : ""}`}
                            onClick={() => setSelectedChromosome(chrom.name)}
                          >
                            {chrom.name}
                          </Button>
                        ))}
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>

                {isLoading && (
                  <div className="flex justify-center py-4" aria-live="polite">
                    <div className="h-6 w-6 animate-spin rounded-full border-2 border-[#3c4f3d]/30 border-t-[#de8246]"></div>
                    <span className="sr-only">Loading…</span>
                  </div>
                )}

                {error && (
                  <div
                    role="alert"
                    className="mt-4 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700"
                  >
                    {error}
                  </div>
                )}

                {searchResults.length > 0 && !isLoading && (
                  <div className="mt-6">
                    <div className="mb-2">
                      <h4 className="text-xs font-normal text-[#3c4f3d]/70">
                        {mode === "search" ? (
                          <>
                            Search Results:{" "}
                            <span className="font-medium text-[#3c4f3d]">
                              {searchResults.length} genes
                            </span>
                          </>
                        ) : (
                          <>
                            Genes on {selectedChromosome}:{" "}
                            <span className="font-medium text-[#3c4f3d]">
                              {searchResults.length} found
                            </span>
                          </>
                        )}
                      </h4>
                    </div>

                    <div className="overflow-hidden rounded-md border border-[#3c4f3d]/5">
                      <Table>
                        <TableHeader>
                          <TableRow className="bg-[#e9eeea]/50 hover:bg-[#e9eeea]/70">
                            <TableHead className="text-xs font-normal text-[#3c4f3d]/70">
                              Symbol
                            </TableHead>
                            <TableHead className="text-xs font-normal text-[#3c4f3d]/70">
                              Name
                            </TableHead>
                            <TableHead className="text-xs font-normal text-[#3c4f3d]/70">
                              Location
                            </TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {searchResults.map((gene, index) => (
                            <TableRow
                              key={`${gene.symbol}-${index}`}
                              tabIndex={0}
                              role="button"
                              aria-label={`Open gene ${gene.symbol}`}
                              className="cursor-pointer border-b border-[#3c4f3d]/5 hover:bg-[#e9eeea]/50 focus-visible:bg-[#e9eeea]/50 outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#de8246]/50 hover:-translate-y-px transition-[background-color,transform] duration-150 ease-[var(--ease-micro)]"
                              onClick={() => setSelectedGene(gene)}
                              onKeyDown={(e) => {
                                if (e.key === "Enter" || e.key === " ") {
                                  e.preventDefault();
                                  setSelectedGene(gene);
                                }
                              }}
                            >
                              <TableCell className="py-2 font-medium text-[#3c4f3d]">
                                {gene.symbol}
                              </TableCell>
                              <TableCell className="py-2 font-medium text-[#3c4f3d]">
                                {gene.name}
                              </TableCell>
                              <TableCell className="py-2 font-medium text-[#3c4f3d]">
                                {gene.chrom}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </div>
                )}

                {!isLoading && !error && searchResults.length === 0 && (
                  <div className="flex h-48 flex-col items-center justify-center text-center text-[#3c4f3d]/40">
                    <Search className="mb-4 h-10 w-10 text-[#3c4f3d]/40" />
                    <p className="text-sm leading-relaxed">
                      {mode === "search"
                        ? "Enter a gene or symbol, then click Search"
                        : selectedChromosome
                          ? "No genes found on this chromosome"
                          : "Select a chromosome to view genes"}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  );
}
