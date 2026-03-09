export interface ChatAttachment {
  library_item_id: string;
  file_name?: string | null;
  mime_type?: string | null;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  advice_type?: string;
  attachments?: ChatAttachment[];
}
