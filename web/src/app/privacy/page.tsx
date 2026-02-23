import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy — StewardMe",
};

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-2xl px-6 py-16">
      <h1 className="text-2xl font-semibold">Privacy Policy</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Last updated: February 23, 2026
      </p>

      <div className="mt-8 space-y-6 text-sm leading-relaxed">
        <section>
          <h2 className="text-lg font-medium">1. Information We Collect</h2>
          <p className="mt-2">
            When you sign in via GitHub or Google, we receive your name, email
            address, and profile photo from the OAuth provider. We also store
            journal entries, goals, and preferences you create within the app.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">2. How We Use Your Information</h2>
          <p className="mt-2">
            Your data is used solely to provide and improve the StewardMe
            service — generating personalized advice, tracking goals, and
            surfacing relevant intelligence. We do not sell your data to third
            parties.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">3. LLM API Keys</h2>
          <p className="mt-2">
            API keys you provide are encrypted at rest and stored per-user. They
            are only used server-side to call your chosen LLM provider on your
            behalf. Keys are never logged or shared.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">4. Data Storage</h2>
          <p className="mt-2">
            Journal entries are stored as markdown files. Intelligence data is
            stored in SQLite. Embeddings are stored in ChromaDB. All data
            resides on the server infrastructure you deploy to.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">5. Third-Party Services</h2>
          <p className="mt-2">
            We integrate with GitHub and Google for authentication, and with LLM
            providers (Anthropic, OpenAI, Google) for AI features. Each
            provider&apos;s own privacy policy applies to data sent to their APIs.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">6. Data Deletion</h2>
          <p className="mt-2">
            You can delete your journal entries, goals, and recommendations at
            any time through the app. To request full account deletion, contact
            us at the email below.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-medium">7. Contact</h2>
          <p className="mt-2">
            For privacy-related questions, contact us at{" "}
            <a href="mailto:privacy@stewardme.ai" className="text-primary underline">
              privacy@stewardme.ai
            </a>.
          </p>
        </section>
      </div>
    </div>
  );
}
