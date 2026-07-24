"use client";

import { useEffect, useState } from "react";
import "@/lib/amplify-config";
import {
  fetchAuthSession,
  getCurrentUser,
  signOut,
} from "aws-amplify/auth";

export default function DashboardPage() {
  const [email, setEmail] = useState("");
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [apiMessage, setApiMessage] = useState("");
  const [isTestingApi, setIsTestingApi] = useState(false);

  useEffect(() => {
    async function verifySession() {
      try {
        const user = await getCurrentUser();
        const session = await fetchAuthSession();

        if (!session.tokens?.idToken) {
          window.location.href = "/signin";
          return;
        }

        setEmail(user.signInDetails?.loginId ?? "Authenticated user");
      } catch {
        window.location.href = "/signin";
      } finally {
        setIsCheckingAuth(false);
      }
    }

    verifySession();
  }, []);

  async function handleProtectedApiTest() {
    setApiMessage("");

    try {
      setIsTestingApi(true);

      const apiBaseUrl = process.env.NEXT_PUBLIC_MERIT_API_BASE_URL;

      if (!apiBaseUrl) {
        throw new Error("MERIT API URL is not configured.");
      }

      const session = await fetchAuthSession();
      const idToken = session.tokens?.idToken?.toString();

      if (!idToken) {
        throw new Error("No authenticated Cognito token is available.");
      }

      const response = await fetch(
        `${apiBaseUrl.replace(/\/$/, "")}/auth-test`,
        {
          method: "GET",
          headers: {
            Authorization: idToken,
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Protected API returned HTTP ${response.status}.`
        );
      }

      setApiMessage(
        "Protected API authorized successfully — HTTP 200 ✅"
      );
    } catch (error) {
      setApiMessage(
        error instanceof Error
          ? error.message
          : "Unable to call the protected API."
      );
    } finally {
      setIsTestingApi(false);
    }
  }

  async function handleSignOut() {
    await signOut();
    window.location.href = "/";
  }

  if (isCheckingAuth) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-100">
        <p className="text-slate-400">Verifying secure session...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
      <div className="mx-auto max-w-6xl">
        <header className="flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-violet-400">
              MERIT
            </p>

            <h1 className="mt-2 text-3xl font-bold">
              Research Intelligence Dashboard
            </h1>

            <p className="mt-2 text-sm text-slate-400">
              Signed in as {email}
            </p>
          </div>

          <button
            type="button"
            onClick={handleSignOut}
            className="rounded-xl border border-slate-700 px-4 py-2 font-medium text-slate-200 transition hover:border-slate-500 hover:text-white"
          >
            Sign out
          </button>
        </header>

        <section className="mt-10 grid gap-5 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm text-slate-400">Documents</p>
            <p className="mt-2 text-3xl font-bold">0</p>
            <p className="mt-2 text-sm text-slate-500">
              Secure document upload arrives in Milestone 4.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm text-slate-400">Processing</p>
            <p className="mt-2 text-3xl font-bold">0</p>
            <p className="mt-2 text-sm text-slate-500">
              Event-driven processing arrives in Milestone 5.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm text-slate-400">Questions</p>
            <p className="mt-2 text-3xl font-bold">0</p>
            <p className="mt-2 text-sm text-slate-500">
              Grounded question answering arrives in Milestone 8.
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <p className="text-sm font-medium text-violet-400">
            Authentication verification
          </p>

          <h2 className="mt-2 text-xl font-semibold">
            Protected API test
          </h2>

          <p className="mt-2 text-sm text-slate-400">
            Send your authenticated Cognito session token to the protected
            MERIT API Gateway route.
          </p>

          <button
            type="button"
            onClick={handleProtectedApiTest}
            disabled={isTestingApi}
            className="mt-5 rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isTestingApi
              ? "Testing protected API..."
              : "Test protected API"}
          </button>

          {apiMessage && (
            <p
              role="status"
              className="mt-4 text-sm text-amber-300"
            >
              {apiMessage}
            </p>
          )}
        </section>
      </div>
    </main>
  );
}