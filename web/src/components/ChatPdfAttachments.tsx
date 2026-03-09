"use client";

import { useRef } from "react";
import { FileText, Paperclip, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { PendingChatPdfAttachment } from "@/hooks/useChatPdfAttachments";
import type { ChatAttachment } from "@/types/chat";

export function ChatAttachmentBadges({
  attachments,
  className = "mb-2",
}: {
  attachments?: ChatAttachment[];
  className?: string;
}) {
  if (!attachments?.length) return null;

  return (
    <div className={`${className} flex flex-wrap gap-1.5`}>
      {attachments.map((attachment) => (
        <Badge
          key={`${attachment.library_item_id}-${attachment.file_name || "pdf"}`}
          variant="outline"
          className="max-w-full"
        >
          <FileText className="h-3 w-3" />
          <span className="truncate">{attachment.file_name || "PDF document"}</span>
        </Badge>
      ))}
    </div>
  );
}

export function ChatPdfAttachmentPicker({
  attachments,
  disabled,
  onAddFiles,
  onRemove,
}: {
  attachments: PendingChatPdfAttachment[];
  disabled?: boolean;
  onAddFiles: (files: FileList | File[] | null | undefined) => void;
  onRemove: (key: string) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div className="space-y-2">
      {attachments.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {attachments.map((attachment) => (
            <Badge key={attachment.key} variant="secondary" className="max-w-full pr-1">
              <FileText className="h-3 w-3" />
              <span className="max-w-[180px] truncate">{attachment.file.name}</span>
              <button
                type="button"
                aria-label={`Remove ${attachment.file.name}`}
                className="rounded-full p-0.5 hover:bg-black/10"
                onClick={() => onRemove(attachment.key)}
                disabled={disabled}
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}
      <div className="flex flex-wrap items-center gap-2">
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          multiple
          className="hidden"
          onChange={(event) => {
            onAddFiles(event.target.files);
            event.currentTarget.value = "";
          }}
          disabled={disabled}
        />
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="gap-2"
          onClick={() => inputRef.current?.click()}
          disabled={disabled}
        >
          <Paperclip className="h-3.5 w-3.5" />
          Attach PDF
        </Button>
        <span className="text-xs text-muted-foreground">
          Uploads to your Library and uses the extracted text in this chat.
        </span>
      </div>
    </div>
  );
}
