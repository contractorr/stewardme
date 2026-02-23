"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Pencil, Check, X, RefreshCw } from "lucide-react";
import { useToken } from "@/hooks/useToken";
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
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
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

interface ProfileData {
  current_role: string;
  career_stage: string;
  skills: { name: string; proficiency: number }[];
  interests: string[];
  aspirations: string;
  location: string;
  languages_frameworks: string[];
  learning_style: string;
  weekly_hours_available: number;
  goals_short_term: string;
  goals_long_term: string;
  industries_watching: string[];
  technologies_watching: string[];
  constraints: Record<string, unknown>;
  fears_risks: string[];
  active_projects: string[];
  updated_at: string | null;
  summary: string;
  is_stale: boolean;
}

// Editable field config
type FieldType = "text" | "textarea" | "tags" | "skills";

interface FieldConfig {
  key: keyof ProfileData;
  label: string;
  type: FieldType;
}

const PROFILE_FIELDS: FieldConfig[] = [
  { key: "current_role", label: "Role", type: "text" },
  { key: "career_stage", label: "Career Stage", type: "text" },
  { key: "skills", label: "Skills", type: "skills" },
  { key: "interests", label: "Interests", type: "tags" },
  { key: "languages_frameworks", label: "Languages & Frameworks", type: "tags" },
  { key: "goals_short_term", label: "6-Month Goals", type: "textarea" },
  { key: "goals_long_term", label: "3-Year Vision", type: "textarea" },
  { key: "aspirations", label: "Aspirations", type: "textarea" },
  { key: "industries_watching", label: "Industries Watching", type: "tags" },
  { key: "technologies_watching", label: "Technologies Watching", type: "tags" },
  { key: "active_projects", label: "Active Projects", type: "tags" },
  { key: "fears_risks", label: "Risks & Concerns", type: "tags" },
  { key: "location", label: "Location", type: "text" },
  { key: "learning_style", label: "Learning Style", type: "text" },
];

function TagsEditor({
  value,
  onChange,
}: {
  value: string[];
  onChange: (v: string[]) => void;
}) {
  const [input, setInput] = useState("");
  const add = () => {
    const tag = input.trim();
    if (tag && !value.includes(tag)) {
      onChange([...value, tag]);
    }
    setInput("");
  };
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-1">
        {value.map((t) => (
          <Badge key={t} variant="secondary" className="gap-1">
            {t}
            <button
              onClick={() => onChange(value.filter((v) => v !== t))}
              className="ml-0.5 hover:text-destructive"
            >
              <X className="h-3 w-3" />
            </button>
          </Badge>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
          placeholder="Add item..."
          className="h-8 text-sm"
        />
        <Button size="sm" variant="outline" onClick={add} className="h-8">
          Add
        </Button>
      </div>
    </div>
  );
}

function SkillsEditor({
  value,
  onChange,
}: {
  value: { name: string; proficiency: number }[];
  onChange: (v: { name: string; proficiency: number }[]) => void;
}) {
  const [input, setInput] = useState("");
  const add = () => {
    const name = input.trim();
    if (name && !value.find((s) => s.name === name)) {
      onChange([...value, { name, proficiency: 3 }]);
    }
    setInput("");
  };
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-1">
        {value.map((s) => (
          <Badge key={s.name} variant="secondary" className="gap-1">
            {s.name} ({s.proficiency})
            <button
              onClick={() => onChange(value.filter((v) => v.name !== s.name))}
              className="ml-0.5 hover:text-destructive"
            >
              <X className="h-3 w-3" />
            </button>
          </Badge>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
          placeholder="Add skill..."
          className="h-8 text-sm"
        />
        <Button size="sm" variant="outline" onClick={add} className="h-8">
          Add
        </Button>
      </div>
    </div>
  );
}

function ProfileField({
  config,
  profile,
  token,
  onUpdated,
}: {
  config: FieldConfig;
  profile: ProfileData;
  token: string;
  onUpdated: (p: ProfileData) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState<unknown>(null);
  const [saving, setSaving] = useState(false);

  const rawValue = profile[config.key];

  const startEdit = () => {
    setDraft(
      config.type === "tags" || config.type === "skills"
        ? JSON.parse(JSON.stringify(rawValue))
        : rawValue
    );
    setEditing(true);
  };

  const cancel = () => {
    setEditing(false);
    setDraft(null);
  };

  const save = async () => {
    setSaving(true);
    try {
      await apiFetch(
        "/api/profile",
        { method: "PATCH", body: JSON.stringify({ [config.key]: draft }) },
        token
      );
      const updated = await apiFetch<ProfileData>("/api/profile", {}, token);
      onUpdated(updated);
      setEditing(false);
      toast.success(`${config.label} updated`);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  // Display value
  const displayValue = () => {
    if (config.type === "skills") {
      const skills = rawValue as { name: string; proficiency: number }[];
      if (!skills.length) return <span className="text-muted-foreground text-sm">Not set</span>;
      return (
        <div className="flex flex-wrap gap-1">
          {skills.map((s) => (
            <Badge key={s.name} variant="outline" className="text-xs">
              {s.name} ({s.proficiency})
            </Badge>
          ))}
        </div>
      );
    }
    if (config.type === "tags") {
      const tags = rawValue as string[];
      if (!tags.length) return <span className="text-muted-foreground text-sm">Not set</span>;
      return (
        <div className="flex flex-wrap gap-1">
          {tags.map((t) => (
            <Badge key={t} variant="outline" className="text-xs">
              {t}
            </Badge>
          ))}
        </div>
      );
    }
    const str = String(rawValue || "");
    if (!str) return <span className="text-muted-foreground text-sm">Not set</span>;
    return <span className="text-sm">{str}</span>;
  };

  return (
    <div className="flex items-start gap-2 py-2">
      <div className="flex-1 min-w-0">
        <Label className="text-xs text-muted-foreground">{config.label}</Label>
        {editing ? (
          <div className="mt-1 space-y-2">
            {config.type === "text" && (
              <Input
                value={draft as string}
                onChange={(e) => setDraft(e.target.value)}
                className="h-8 text-sm"
              />
            )}
            {config.type === "textarea" && (
              <Textarea
                value={draft as string}
                onChange={(e) => setDraft(e.target.value)}
                rows={3}
                className="text-sm"
              />
            )}
            {config.type === "tags" && (
              <TagsEditor
                value={draft as string[]}
                onChange={(v) => setDraft(v)}
              />
            )}
            {config.type === "skills" && (
              <SkillsEditor
                value={draft as { name: string; proficiency: number }[]}
                onChange={(v) => setDraft(v)}
              />
            )}
            <div className="flex gap-1">
              <Button size="sm" variant="outline" onClick={save} disabled={saving} className="h-7 text-xs">
                <Check className="mr-1 h-3 w-3" />
                Save
              </Button>
              <Button size="sm" variant="ghost" onClick={cancel} className="h-7 text-xs">
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <div className="mt-0.5">{displayValue()}</div>
        )}
      </div>
      {!editing && (
        <Button size="icon" variant="ghost" onClick={startEdit} className="h-7 w-7 shrink-0 mt-3">
          <Pencil className="h-3 w-3" />
        </Button>
      )}
    </div>
  );
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
  const router = useRouter();
  const [settings, setSettings] = useState<Settings | null>(null);
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [form, setForm] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  const isDirty = Object.keys(form).length > 0;

  useEffect(() => {
    if (!token) return;
    apiFetch<Settings>("/api/settings", {}, token)
      .then(setSettings)
      .catch((e) => toast.error(e.message));
    apiFetch<ProfileData>("/api/profile", {}, token)
      .then(setProfile)
      .catch(() => {}); // profile may not exist yet
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
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Profile</CardTitle>
              <CardDescription>
                Your profile context — used to personalise advice and recommendations
              </CardDescription>
            </div>
            {profile?.is_stale && (
              <Badge variant="secondary" className="text-xs">Stale</Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {profile && token ? (
            <div className="divide-y">
              {PROFILE_FIELDS.map((f) => (
                <ProfileField
                  key={f.key}
                  config={f}
                  profile={profile}
                  token={token}
                  onUpdated={setProfile}
                />
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No profile yet. Complete onboarding to create one.
            </p>
          )}
          <Separator className="my-4" />
          <Button variant="outline" onClick={() => router.push("/onboarding")}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Restart Onboarding
          </Button>
        </CardContent>
      </Card>

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
