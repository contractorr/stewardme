"use client";

import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
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
}

export function ApiKeyInput({
  label,
  name,
  value,
  onChange,
  isSet,
  hint,
}: ApiKeyInputProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="space-y-1.5">
      <div className="flex items-center gap-2">
        <Label htmlFor={name}>{label}</Label>
        {isSet && (
          <Badge variant="secondary" className="text-xs">
            Set{hint ? ` (${hint})` : ""}
          </Badge>
        )}
      </div>
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
    </div>
  );
}
