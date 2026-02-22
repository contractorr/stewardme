"use client";

import { useState } from "react";
import { AlertCircle, Eye, EyeOff } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface ApiKeyInputProps {
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  isSet: boolean;
  hint?: string | null;
  description?: string;
}

export function ApiKeyInput({
  label,
  name,
  value,
  onChange,
  isSet,
  hint,
  description,
}: ApiKeyInputProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="space-y-1.5">
      <div className="flex items-center gap-2">
        <Label htmlFor={name}>{label}</Label>
        {isSet && (
          <Badge
            variant="outline"
            className="border-emerald-600 text-emerald-600 text-xs"
          >
            Configured{hint ? ` (${hint})` : ""}
          </Badge>
        )}
      </div>
      {description && (
        <p className="text-xs text-muted-foreground">{description}</p>
      )}
      <div className="relative">
        <Input
          id={name}
          type={visible ? "text" : "password"}
          placeholder={isSet ? "Enter new value to replace" : "Enter key"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="pr-10"
        />
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="absolute right-0 top-0 h-full px-3"
          onClick={() => setVisible(!visible)}
        >
          {visible ? (
            <EyeOff className="h-4 w-4" />
          ) : (
            <Eye className="h-4 w-4" />
          )}
        </Button>
      </div>
      {isSet && value && (
        <div className="flex items-center gap-1.5 text-xs text-amber-600">
          <AlertCircle className="h-3.5 w-3.5" />
          <span>Will replace existing value</span>
        </div>
      )}
    </div>
  );
}
