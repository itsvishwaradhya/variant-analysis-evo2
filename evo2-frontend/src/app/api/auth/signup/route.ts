import { NextResponse } from "next/server";
import { z } from "zod";
import {
  AUTH_COOKIE,
  authCookieOptions,
  hashPassword,
  signJWT,
} from "~/lib/auth";
import { connectDB } from "~/lib/mongodb";
import { User } from "~/models/User";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
});

export async function POST(req: Request) {
  const body = schema.safeParse(await req.json().catch(() => null));
  if (!body.success) {
    return NextResponse.json({ error: "Invalid email or password" }, { status: 400 });
  }
  await connectDB();
  const email = body.data.email.toLowerCase().trim();
  const existing = await User.findOne({ email }).lean();
  if (existing) {
    return NextResponse.json({ error: "Email already registered" }, { status: 409 });
  }
  const passwordHash = await hashPassword(body.data.password);
  const user = await User.create({ email, passwordHash });
  const token = await signJWT({ sub: String(user._id), email });
  const res = NextResponse.json(
    { user: { id: String(user._id), email } },
    { status: 201 },
  );
  res.cookies.set(AUTH_COOKIE, token, authCookieOptions());
  return res;
}
