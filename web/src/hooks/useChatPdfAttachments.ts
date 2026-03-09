"use client";

import { useCallback, useState } from "react";
import { toast } from "sonner";
import { apiFetch } from "@/lib/api";
import type { ChatAttachmentUpload } from "@/types/library";

const MAX_ATTACHMENTS = 5;

export interface PendingChatPdfAttachment {
  key: string;
  file: File;
}

function fileKey(file: File): string {
  return `${file.name}-${file.size}-${file.lastModified}`;
}

function isPdf(file: File): boolean {
  return file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
}

export function useChatPdfAttachments(token?: string) {
  const [attachments, setAttachments] = useState<PendingChatPdfAttachment[]>([]);
  const [uploading, setUploading] = useState(false);

  const addFiles = useCallback((incoming: FileList | File[] | null | undefined) => {
    const files = Array.from(incoming || []);
    if (!files.length) return;

    const invalidNames = files.filter((file) => !isPdf(file)).map((file) => file.name);
    if (invalidNames.length) {
      toast.error(`Only PDF files are supported: ${invalidNames.join(", ")}`);
    }

    setAttachments((current) => {
      const existing = new Set(current.map((item) => item.key));
      const next = [...current];

      for (const file of files) {
        if (!isPdf(file)) continue;
        const key = fileKey(file);
        if (existing.has(key)) continue;
        if (next.length >= MAX_ATTACHMENTS) {
          toast.error(`You can attach up to ${MAX_ATTACHMENTS} PDFs per message.`);
          break;
        }
        next.push({ key, file });
        existing.add(key);
      }

      return next;
    });
  }, []);

  const removeAttachment = useCallback((key: string) => {
    setAttachments((current) => current.filter((item) => item.key !== key));
  }, []);

  const clearAttachments = useCallback(() => {
    setAttachments([]);
  }, []);

  const uploadPending = useCallback(async (): Promise<ChatAttachmentUpload[]> => {
    if (!attachments.length) return [];
    if (!token) {
      throw new Error("You need to be signed in to upload PDFs.");
    }

    setUploading(true);
    try {
      const uploaded: ChatAttachmentUpload[] = [];
      for (const attachment of attachments) {
        const formData = new FormData();
        formData.append("file", attachment.file);
        uploaded.push(
          await apiFetch<ChatAttachmentUpload>(
            "/api/advisor/attachments",
            { method: "POST", body: formData },
            token,
          ),
        );
      }
      setAttachments([]);
      return uploaded;
    } finally {
      setUploading(false);
    }
  }, [attachments, token]);

  return {
    attachments,
    addFiles,
    removeAttachment,
    clearAttachments,
    uploadPending,
    uploading,
    hasAttachments: attachments.length > 0,
  };
}
