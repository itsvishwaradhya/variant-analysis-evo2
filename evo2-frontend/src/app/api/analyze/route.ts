import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { z } from "zod";
import { AUTH_COOKIE, verifyJWT } from "~/lib/auth";
import { env } from "~/env";

const schema = z.object({
  variant_position: z.number().int(),
  alternative: z.string().regex(/^[ATGC]$/),
  genome: z.string().min(1),
  chromosome: z.string().min(1),
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
