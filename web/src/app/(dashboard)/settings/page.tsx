"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { RefreshCw } from "lucide-react";
import { useToken } from "@/hooks/useToken";
import { OnboardingDialog } from "@/components/OnboardingDialog";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { ApiKeyInput } from "@/components/ApiKeyInput";
import { apiFetch } from "@/lib/api";

interface Settings {
  llm_provider: string | null;
  llm_model: string | null;
  llm_api_key_set: boolean;
  llm_api_key_hint: string | null;
  tavily_api_key_set: boolean;
  tavily_api_key_hint: string | null;
  github_token_set: boolean;
  github_token_hint: string | null;
  eventbrite_token_set: boolean;
}

function SettingsSkeleton() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      <div className="h-7 w-24 animate-pulse rounded bg-muted" />
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <div className="h-5 w-32 animate-pulse rounded bg-muted" />
            <div className="h-3 w-48 animate-pulse rounded bg-muted" />
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="h-9 w-full animate-pulse rounded bg-muted" />
            <div className="h-9 w-full animate-pulse rounded bg-muted" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default function SettingsPage() {
  const token = useToken();
  const [settings, setSettings] = useState<Settings | null>(null);
  const [form, setForm] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);

  const isDirty = Object.keys(form).length > 0;

  useEffect(() => {
    if (!token) return;
    apiFetch<Settings>("/api/settings", {}, token)
      .then(setSettings)
      .catch((e) => toast.error(e.message));
  }, [token]);

  const handleSave = async () => {
    if (!token) return;
    setSaving(true);
    try {
      const payload: Record<string, string | number> = {};
      for (const [key, val] of Object.entries(form)) {
        if (val) payload[key] = val;
      }
      const updated = await apiFetch<Settings>(
        "/api/settings",
        { method: "PUT", body: JSON.stringify(payload) },
        token
      );
      setSettings(updated);
      setForm({});
      toast.success("Settings saved");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (!settings) return <SettingsSkeleton />;

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Settings</h1>

      <Card>
        <CardHeader>
          <CardTitle>LLM Provider</CardTitle>
          <CardDescription>Configure your AI model provider</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <Label>Provider</Label>
            <p className="text-xs text-muted-foreground">Auto-detect picks provider based on your API key.</p>
            <Select
              value={form.llm_provider || settings.llm_provider || "auto"}
              onValueChange={(v) => setForm({ ...form, llm_provider: v })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="auto">Auto-detect</SelectItem>
                <SelectItem value="claude">Claude</SelectItem>
                <SelectItem value="openai">OpenAI</SelectItem>
                <SelectItem value="gemini">Gemini</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1.5">
            <Label>Model (optional)</Label>
            <p className="text-xs text-muted-foreground">Leave blank for the provider&apos;s default model.</p>
            <Input
              placeholder="e.g. claude-sonnet-4-20250514"
              value={form.llm_model || ""}
              onChange={(e) => setForm({ ...form, llm_model: e.target.value })}
            />
          </div>
          <ApiKeyInput
            label="LLM API Key"
            name="llm_api_key"
            value={form.llm_api_key || ""}
            onChange={(v) => setForm({ ...form, llm_api_key: v })}
            isSet={settings.llm_api_key_set}
            hint={settings.llm_api_key_hint}
            description="Required. Powers the Advisor. Your key is encrypted and stored per-user."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>API Keys</CardTitle>
          <CardDescription>Keys for intelligence and research</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ApiKeyInput
            label="Tavily API Key"
            name="tavily_api_key"
            value={form.tavily_api_key || ""}
            onChange={(v) => setForm({ ...form, tavily_api_key: v })}
            isSet={settings.tavily_api_key_set}
            hint={settings.tavily_api_key_hint}
            description="Optional. Enables web search for deep research. Falls back to DuckDuckGo if not set."
          />
          <ApiKeyInput
            label="GitHub Token"
            name="github_token"
            value={form.github_token || ""}
            onChange={(v) => setForm({ ...form, github_token: v })}
            isSet={settings.github_token_set}
            hint={settings.github_token_hint}
            description="Optional. Raises GitHub scraper rate limit from 60 to 5,000 req/hr. Needs only public_repo scope."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
          <CardDescription>Re-run the onboarding interview to update your profile and goals</CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" onClick={() => setShowOnboarding(true)}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Restart Onboarding
          </Button>
        </CardContent>
      </Card>

      {token && (
        <OnboardingDialog
          open={showOnboarding}
          onClose={() => setShowOnboarding(false)}
          onComplete={() => {
            apiFetch<Settings>("/api/settings", {}, token!)
              .then(setSettings)
              .catch(() => {});
          }}
          token={token}
          startPhase={settings.llm_api_key_set ? "chat" : "intro"}
        />
      )}

      <Separator />
      <div className="flex items-center gap-3">
        <Button onClick={handleSave} disabled={saving || !isDirty}>
          {saving ? "Saving..." : isDirty ? "Save Changes" : "No Changes"}
        </Button>
        {isDirty && (
          <span className="text-xs text-muted-foreground">
            {Object.keys(form).length} unsaved {Object.keys(form).length === 1 ? "change" : "changes"}
          </span>
        )}
      </div>
    </div>
  );
}
