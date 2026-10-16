import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { z } from "zod";
import { AUTH_COOKIE, verifyJWT } from "~/lib/auth";
import { env } from "~/env";

const schema = z
  .object({
    variant_position: z.number().int().positive(),
    variant_type: z
      .enum(["snv", "deletion", "insertion", "delins"])
      .optional()
      .default("snv"),
    alternative: z.string().optional(),
    deletion_length: z.number().int().min(1).max(500).optional(),
    inserted_sequence: z
      .string()
      .regex(/^[ATGCatgc\s]+$/)
      .max(500)
      .optional(),
    genome: z.string().min(1),
    chromosome: z.string().min(1),
  })
  .superRefine((val, ctx) => {
    const fail = (message: string, path: (string | number)[]) =>
      ctx.addIssue({ code: z.ZodIssueCode.custom, message, path });
    if (val.variant_type === "deletion") {
      if (val.deletion_length == null) {
        fail("deletion_length is required for deletion", ["deletion_length"]);
      }
      if (val.alternative != null && val.alternative !== "" && val.alternative !== "-") {
        fail("alternative must not be set for deletion", ["alternative"]);
      }
      if (val.inserted_sequence != null && val.inserted_sequence !== "") {
        fail("inserted_sequence must not be set for deletion (use delins)", [
          "inserted_sequence",
        ]);
      }
    } else if (val.variant_type === "insertion") {
      const seq = (val.inserted_sequence ?? "").replace(/\s+/g, "").toUpperCase();
      if (!/^[ATGC]+$/.test(seq)) {
        fail("inserted_sequence must be 1-500bp of A, T, C, G", [
          "inserted_sequence",
        ]);
      }
      if (val.deletion_length != null) {
        fail("deletion_length must not be set for insertion (use delins)", [
          "deletion_length",
        ]);
      }
      if (val.alternative != null && val.alternative !== "" && val.alternative !== "-") {
        fail("alternative must not be set for insertion", ["alternative"]);
      }
    } else if (val.variant_type === "delins") {
      if (val.deletion_length == null) {
        fail("deletion_length is required for delins", ["deletion_length"]);
      }
      const seq = (val.inserted_sequence ?? "").replace(/\s+/g, "").toUpperCase();
      if (!/^[ATGC]+$/.test(seq)) {
        fail("inserted_sequence must be 1-500bp of A, T, C, G", [
          "inserted_sequence",
        ]);
      }
      if (val.alternative != null && val.alternative !== "" && val.alternative !== "-") {
        fail("alternative must not be set for delins", ["alternative"]);
      }
    } else {
      if (!val.alternative || !/^[ATGC]$/.test(val.alternative)) {
        fail("alternative must be one of A, T, C, G", ["alternative"]);
      }
      if (val.deletion_length != null) {
        fail("deletion_length must not be set for SNV", ["deletion_length"]);
      }
      if (val.inserted_sequence != null && val.inserted_sequence !== "") {
        fail("inserted_sequence must not be set for SNV", ["inserted_sequence"]);
      }
    }
  });

export async function POST(req: Request) {
  const token = (await cookies()).get(AUTH_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  }
  try {
    await verifyJWT(token);
  } catch {
    return NextResponse.json({ error: "Session expired, sign in again" }, { status: 401 });
  }

  const body = schema.safeParse(await req.json().catch(() => null));
  if (!body.success) {
    return NextResponse.json({ error: "Invalid variant payload" }, { status: 400 });
  }

  const upstream = await fetch(env.NEXT_PUBLIC_ANALYZE_SINGLE_VARIANT_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body.data),
  });

  const text = await upstream.text();
  if (!upstream.ok) {
    return NextResponse.json(
      { error: `Analysis failed: ${text.slice(0, 300)}` },
      { status: upstream.status },
    );
  }
  try {
    return NextResponse.json(JSON.parse(text));
  } catch {
    return NextResponse.json({ error: "Bad upstream response" }, { status: 502 });
  }
}
