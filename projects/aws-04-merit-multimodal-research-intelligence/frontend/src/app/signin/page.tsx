"use client";

import { FormEvent, useState } from "react";
import "@/lib/amplify-config";
import { signIn } from "aws-amplify/auth";
import Link from "next/link";

export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");

    try {
      setIsLoading(true);

      const result = await signIn({
        username: email.trim(),
        password,
      });

      if (result.isSignedIn) {
        window.location.href = "/dashboard";
        return;
      }

      if (result.nextStep.signInStep === "CONFIRM_SIGN_UP") {
        sessionStorage.setItem("merit-signup-email", email.trim());
        window.location.href = "/confirm-signup";
        return;
      }

      setMessage(
        `Additional authentication step required: ${result.nextStep.signInStep}`
      );
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Unable to sign in."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl">
        <Link
          href="/"
          className="text-sm font-medium text-violet-400 hover:text-violet-300"
        >
          ← Back to MERIT
        </Link>

        <div className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
            MERIT
          </p>

          <h1 className="mt-2 text-3xl font-bold">Sign in</h1>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Access your secure research-intelligence workspace.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-violet-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-violet-500"
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? "Signing in..." : "Sign in"}
          </button>

          {message && (
            <p role="alert" className="text-sm text-amber-300">
              {message}
            </p>
          )}
        </form>

        <div className="mt-6 flex items-center justify-between text-sm">
          <a
            href="/forgot-password"
            className="text-violet-400 hover:text-violet-300"
          >
            Forgot password?
          </a>

          <a
            href="/register"
            className="text-slate-300 hover:text-white"
          >
            Create account
          </a>
        </div>
      </div>
    </main>
  );
}