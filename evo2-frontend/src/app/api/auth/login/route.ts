import { NextResponse } from "next/server";
import { z } from "zod";
import {
  AUTH_COOKIE,
  authCookieOptions,
  signJWT,
  verifyPassword,
} from "~/lib/auth";
import { connectDB } from "~/lib/mongodb";
import { User } from "~/models/User";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1).max(100),
});

export async function POST(req: Request) {
  const body = schema.safeParse(await req.json().catch(() => null));
  if (!body.success) {
    return NextResponse.json({ error: "Invalid credentials" }, { status: 400 });
  }
  await connectDB();
  const email = body.data.email.toLowerCase().trim();
  const user = await User.findOne({ email });
  if (!user || !(await verifyPassword(body.data.password, user.passwordHash))) {
    return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
  }
  const token = await signJWT({ sub: String(user._id), email: user.email });
  const res = NextResponse.json({
    user: { id: String(user._id), email: user.email },
  });
  res.cookies.set(AUTH_COOKIE, token, authCookieOptions());
  return res;
}
