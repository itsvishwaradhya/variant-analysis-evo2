import bcrypt from "bcryptjs";
import { jwtVerify, SignJWT } from "jose";
import { env } from "~/env";

const secret = () => new TextEncoder().encode(env.JWT_SECRET);
const COOKIE = "token";
const EXPIRES_IN = "7d";
const MAX_AGE = 60 * 60 * 24 * 7;

export const AUTH_COOKIE = COOKIE;
export const AUTH_MAX_AGE = MAX_AGE;

export async function hashPassword(password: string) {
  return bcrypt.hash(password, 10);
}

export async function verifyPassword(password: string, hash: string) {
  return bcrypt.compare(password, hash);
}

export async function signJWT(payload: { sub: string; email: string }) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(EXPIRES_IN)
    .sign(secret());
}

export async function verifyJWT(token: string) {
  const { payload } = await jwtVerify(token, secret());
  return payload as { sub: string; email: string; exp?: number };
}

export function authCookieOptions() {
  return {
    httpOnly: true as const,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE,
  };
}
