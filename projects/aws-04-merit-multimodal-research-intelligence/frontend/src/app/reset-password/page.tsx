"use client";

import { FormEvent, useEffect, useState } from "react";
import "@/lib/amplify-config";
import { confirmResetPassword } from "aws-amplify/auth";

export default function ResetPasswordPage() {
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const savedEmail = sessionStorage.getItem("merit-reset-email");

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
      setMessage("Enter the email address for your MERIT account.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }

    try {
      setIsLoading(true);

      await confirmResetPassword({
        username: email.trim(),
        confirmationCode: code.trim(),
        newPassword,
      });

      sessionStorage.removeItem("merit-reset-email");
      window.location.href = "/signin?reset=true";
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Unable to reset your password."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 py-12 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl">
        <a
          href="/forgot-password"
          className="text-sm font-medium text-violet-400 hover:text-violet-300"
        >
          ← Back
        </a>

        <div className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
            MERIT
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Choose a new password
          </h1>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Enter the verification code sent to your email and choose a new
            password.
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
              htmlFor="verification-code"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Verification code
            </label>

            <input
              id="verification-code"
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

          <div>
            <label
              htmlFor="new-password"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              New password
            </label>

            <input
              id="new-password"
              type="password"
              autoComplete="new-password"
              required
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-violet-500"
              placeholder="Enter a new password"
            />
          </div>

          <div>
            <label
              htmlFor="confirm-password"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Confirm new password
            </label>

            <input
              id="confirm-password"
              type="password"
              autoComplete="new-password"
              required
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-violet-500"
              placeholder="Repeat your new password"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? "Resetting password..." : "Reset password"}
          </button>

          {message && (
            <p role="alert" className="text-sm text-amber-300">
              {message}
            </p>
          )}
        </form>
      </div>
    </main>
  );
}