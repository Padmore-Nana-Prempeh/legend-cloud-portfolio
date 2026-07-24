export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <main className="mx-auto flex min-h-screen max-w-6xl flex-col px-6 py-12 sm:px-10 lg:px-16">
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-violet-400">
              Legend Cloud Portfolio
            </p>
            <h1 className="mt-2 text-2xl font-bold tracking-tight">
              MERIT
            </h1>
          </div>

          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-300">
            Development
          </span>
        </header>

        <section className="flex flex-1 flex-col justify-center py-20">
          <div className="max-w-4xl">
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
              Multimodal Research Intelligence
            </p>

            <h2 className="text-4xl font-bold tracking-tight sm:text-6xl">
              Evidence retrieval built for trustworthy research.
            </h2>

            <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
              MERIT is the Multimodal Evidence Retrieval and Research
              Intelligence Toolkit — a secure AWS platform for ingesting,
              retrieving, reranking, and synthesizing evidence from research
              documents and multimodal sources.
            </p>

            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">Security</p>
                <p className="mt-2 font-semibold">
                  Private-by-default AWS architecture
                </p>
              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">Retrieval</p>
                <p className="mt-2 font-semibold">
                  Hybrid search + custom reranking
                </p>
              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">Generation</p>
                <p className="mt-2 font-semibold">
                  Grounded answers with citations
                </p>
              </div>
            </div>

            <div className="mt-10 flex flex-wrap items-center gap-4">
              <a
                href="/signin"
                className="rounded-xl bg-violet-500 px-5 py-3 font-semibold text-white transition hover:bg-violet-400"
              >
                Sign in
              </a>

              <a
                href="/register"
                className="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-200 transition hover:border-slate-500"
              >
                Create account
              </a>
            </div>
          </div>
        </section>

        <footer className="border-t border-slate-800 pt-6 text-sm text-slate-500">
          MERIT · Secure multimodal research intelligence on AWS
        </footer>
      </main>
    </div>
  );
}
