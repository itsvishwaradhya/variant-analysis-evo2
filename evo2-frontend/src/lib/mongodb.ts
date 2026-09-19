import mongoose from "mongoose";
import { env } from "~/env";

declare global {
  // eslint-disable-next-line no-var
  var _mongooseConn: Promise<typeof mongoose> | undefined;
}

export async function connectDB() {
  if (mongoose.connection.readyState >= 1) return mongoose;

  global._mongooseConn ??= mongoose.connect(env.MONGODB_URI);
  return global._mongooseConn;
}
