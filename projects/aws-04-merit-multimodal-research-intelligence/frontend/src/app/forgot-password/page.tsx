"use client";

import { FormEvent, useState } from "react";
import "@/lib/amplify-config";
import { resetPassword } from "aws-amplify/auth";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");

    try {
      setIsLoading(true);

      const output = await resetPassword({
        username: email.trim(),
      });

      if (
        output.nextStep.resetPasswordStep ===
        "CONFIRM_RESET_PASSWORD_WITH_CODE"
      ) {
        sessionStorage.setItem("merit-reset-email", email.trim());
        window.location.href = "/reset-password";
        return;
      }

      setMessage(
        `Additional password reset step required: ${output.nextStep.resetPasswordStep}`
      );
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Unable to start password recovery."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl">
        <a
          href="/signin"
          className="text-sm font-medium text-violet-400 hover:text-violet-300"
        >
          ← Back to sign in
        </a>

        <div className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
            MERIT
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Reset your password
          </h1>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Enter your account email and MERIT will send you a verification code.
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

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? "Sending code..." : "Send verification code"}
          </button>

          {message && (
            <p role="alert" className="text-sm text-amber-300">
              {message}
            </p>
          )}
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Remembered your password?{" "}
          <a
            href="/signin"
            className="font-medium text-violet-400 hover:text-violet-300"
          >
            Sign in
          </a>
        </p>
      </div>
    </main>
  );
}