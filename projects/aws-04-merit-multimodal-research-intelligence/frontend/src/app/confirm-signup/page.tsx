"use client";

import { FormEvent, useEffect, useState } from "react";
import "@/lib/amplify-config";
import { confirmSignUp } from "aws-amplify/auth";

export default function ConfirmSignUpPage() {
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const savedEmail = sessionStorage.getItem("merit-signup-email");

    if (!savedEmail) {
      return;
    }

    const timer = window.setTimeout(() => {
      setEmail(savedEmail);
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");

    if (!email.trim()) {
      setMessage("Enter the email address used during registration.");
      return;
    }

    try {
      setIsLoading(true);

      const { nextStep } = await confirmSignUp({
        username: email.trim(),
        confirmationCode: code.trim(),
      });

      if (nextStep.signUpStep === "DONE") {
        sessionStorage.removeItem("merit-signup-email");
        window.location.href = "/signin?confirmed=true";
        return;
      }

      setMessage("Additional confirmation is required.");
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Unable to verify your account."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl">
        <a
          href="/register"
          className="text-sm font-medium text-violet-400 hover:text-violet-300"
        >
          ← Back to registration
        </a>

        <div className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
            MERIT
          </p>

          <h1 className="mt-2 text-3xl font-bold">Verify your email</h1>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Enter the verification code Cognito sent to your email address.
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
              htmlFor="confirmation-code"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Verification code
            </label>

            <input
              id="confirmation-code"
              type="text"
              inputMode="numeric"
              autoComplete="one-time-code"
              required
              value={code}
              onChange={(event) => setCode(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-violet-500"
              placeholder="Enter verification code"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? "Verifying..." : "Verify account"}
          </button>

          {message && (
            <p role="alert" className="text-sm text-amber-300">
              {message}
            </p>
          )}
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Already verified?{" "}
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