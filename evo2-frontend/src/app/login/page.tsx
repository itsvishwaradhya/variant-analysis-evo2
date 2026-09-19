"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Input } from "~/components/ui/input";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch(`/api/auth/${mode}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });
      const data = (await res.json()) as { error?: string };
      if (!res.ok) {
        setError(data.error ?? "Authentication failed");
        return;
      }
      router.push("/");
      router.refresh();
    } catch {
      setError("Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#e9eeea] px-6">
      <Card className="w-full max-w-sm border-none bg-white shadow-sm">
        <CardHeader>
          <CardTitle className="text-lg font-medium text-[#3c4f3d]">
            {mode === "login" ? "Sign in" : "Create account"}
          </CardTitle>
          <p className="text-xs text-[#3c4f3d]/60">
            Sign in to run Evo2 variant analysis. Browsing stays public.
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={submit} className="space-y-3">
            <Input
              type="email"
              required
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="h-9 border-[#3c4f3d]/10"
            />
            <Input
              type="password"
              required
              minLength={8}
              placeholder="Password (min 8 chars)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="h-9 border-[#3c4f3d]/10"
            />
            {error && (
              <div className="rounded-md bg-red-50 p-2 text-xs text-red-600">
                {error}
              </div>
            )}
            <Button
              type="submit"
              disabled={loading}
              className="h-9 w-full cursor-pointer bg-[#3c4f3d] text-white hover:bg-[#3c4f3d]/90"
            >
              {loading
                ? "Please wait..."
                : mode === "login"
                  ? "Sign in"
                  : "Sign up"}
            </Button>
          </form>
          <div className="mt-4 text-center text-xs text-[#3c4f3d]/70">
            {mode === "login" ? (
              <button
                className="cursor-pointer text-[#de8246] hover:underline"
                onClick={() => setMode("signup")}
              >
                Need an account? Sign up
              </button>
            ) : (
              <button
                className="cursor-pointer text-[#de8246] hover:underline"
                onClick={() => setMode("login")}
              >
                Have an account? Sign in
              </button>
            )}
            <div className="mt-2">
              <Link href="/" className="hover:underline">
                Back to browser
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
