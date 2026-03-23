import type { Metadata } from "next";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import Landing from "@/components/landing";

export const metadata: Metadata = {
  title: "StewardMe — An e-bike for the mind",
  description:
    "AI that guides you through new topics, professional growth and personal reflection — grounded in live data, personalised to you.",
  openGraph: {
    title: "StewardMe — An e-bike for the mind",
    description:
      "AI that guides you through new topics, professional growth and personal reflection — grounded in live data, personalised to you.",
    url: "https://stewardme.ai",
    siteName: "StewardMe",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "StewardMe — An e-bike for the mind",
    description:
      "AI that guides you through new topics, professional growth and personal reflection — grounded in live data, personalised to you.",
  },
};

export default async function RootPage() {
  const session = await auth();
  if (session?.user) {
    redirect("/home");
  }
  return <Landing />;
}
