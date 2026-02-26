"use client";

import { useState } from "react";
import { signOut } from "next-auth/react";
import { Dialog } from "radix-ui";
import { toast } from "sonner";
import { useToken } from "@/hooks/useToken";
import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function DeleteAccountModal({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const token = useToken();
  const [confirmation, setConfirmation] = useState("");
  const [deleting, setDeleting] = useState(false);

  const confirmed = confirmation === "DELETE";

  const handleDelete = async () => {
    if (!confirmed || !token) return;
    setDeleting(true);
    try {
      await apiFetch("/api/user/me", { method: "DELETE" }, token);
      toast.success("Account deleted");
      signOut({ callbackUrl: "/login" });
    } catch (e) {
      toast.error((e as Error).message);
      setDeleting(false);
    }
  };

  return (
    <Dialog.Root open={open} onOpenChange={(o) => { if (!deleting) { onOpenChange(o); setConfirmation(""); } }}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-lg border bg-background p-6 shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          <Dialog.Title className="text-lg font-semibold">Delete account</Dialog.Title>
          <Dialog.Description className="mt-2 text-sm text-muted-foreground">
            This will permanently delete your account and all associated data. This action cannot be undone.
          </Dialog.Description>
          <div className="mt-4 space-y-2">
            <label className="text-sm font-medium">
              Type <span className="font-mono font-bold">DELETE</span> to confirm
            </label>
            <Input
              value={confirmation}
              onChange={(e) => setConfirmation(e.target.value)}
              placeholder="DELETE"
              autoComplete="off"
            />
          </div>
          <div className="mt-6 flex justify-end gap-2">
            <Dialog.Close asChild>
              <Button variant="outline" disabled={deleting}>Cancel</Button>
            </Dialog.Close>
            <Button
              variant="destructive"
              disabled={!confirmed || deleting}
              onClick={handleDelete}
            >
              {deleting ? "Deleting..." : "Delete account"}
            </Button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
