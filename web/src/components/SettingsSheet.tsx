"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import { ApiKeyInput } from "@/components/ApiKeyInput";
import { OnboardingDialog } from "@/components/OnboardingDialog";
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

export function SettingsSheet({
  open,
  onOpenChange,
  token,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  token: string;
}) {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [form, setForm] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);

  const isDirty = Object.keys(form).length > 0;

  useEffect(() => {
    if (!open || !token) return;
    apiFetch<Settings>("/api/settings", {}, token)
      .then(setSettings)
      .catch((e) => toast.error(e.message));
  }, [open, token]);

  const handleSave = async () => {
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

  return (
    <>
      <Sheet open={open} onOpenChange={onOpenChange}>
        <SheetContent className="overflow-y-auto">
          <SheetHeader>
            <SheetTitle>Settings</SheetTitle>
            <SheetDescription>Configure your steward&apos;s AI model and API keys</SheetDescription>
          </SheetHeader>

          {!settings ? (
            <div className="space-y-4 px-6 py-4">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="h-9 w-full animate-pulse rounded bg-muted" />
              ))}
            </div>
          ) : (
            <div className="space-y-6 px-6 pb-6">
              {/* LLM Provider */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium">LLM Provider</h3>
                <div className="space-y-1.5">
                  <Label>Provider</Label>
                  <p className="text-xs text-muted-foreground">
                    Auto-detect picks provider based on your API key.
                  </p>
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
                  <p className="text-xs text-muted-foreground">
                    Leave blank for the provider&apos;s default model.
                  </p>
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
                  description="Required. Powers the Advisor."
                />
              </div>

              <Separator />

              {/* Other API Keys */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium">API Keys</h3>
                <ApiKeyInput
                  label="Tavily API Key"
                  name="tavily_api_key"
                  value={form.tavily_api_key || ""}
                  onChange={(v) => setForm({ ...form, tavily_api_key: v })}
                  isSet={settings.tavily_api_key_set}
                  hint={settings.tavily_api_key_hint}
                  description="Optional. Enables web search for deep research."
                />
                <ApiKeyInput
                  label="GitHub Token"
                  name="github_token"
                  value={form.github_token || ""}
                  onChange={(v) => setForm({ ...form, github_token: v })}
                  isSet={settings.github_token_set}
                  hint={settings.github_token_hint}
                  description="Optional. Raises GitHub scraper rate limit."
                />
              </div>

              <Separator />

              {/* Profile */}
              <div className="space-y-2">
                <h3 className="text-sm font-medium">Profile</h3>
                <p className="text-xs text-muted-foreground">
                  Re-run onboarding to update your profile and goals
                </p>
                <Button variant="outline" size="sm" onClick={() => setShowOnboarding(true)}>
                  <RefreshCw className="mr-2 h-3.5 w-3.5" />
                  Restart Onboarding
                </Button>
              </div>

              <Separator />

              <Button onClick={handleSave} disabled={saving || !isDirty} className="w-full">
                {saving ? "Saving..." : isDirty ? "Save Changes" : "No Changes"}
              </Button>
            </div>
          )}
        </SheetContent>
      </Sheet>

      <OnboardingDialog
        open={showOnboarding}
        onClose={() => setShowOnboarding(false)}
        onComplete={() => {
          apiFetch<Settings>("/api/settings", {}, token)
            .then(setSettings)
            .catch(() => {});
        }}
        token={token}
        startPhase={settings?.llm_api_key_set ? "chat" : "intro"}
      />
    </>
  );
}
