"use client";

import { cn } from "../../lib/utils";
import { useState } from "react";

type ToasterProps = {
  type: "success" | "neutral" | "warning" | "error";
  content: string;
  isOpen: boolean;
};

function useToast() {
  const [type, setType] = useState<ToasterProps["type"]>("neutral");
  const [content, setContent] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const toasterElement = Toaster({ type, content, isOpen });

  function toast(type: ToasterProps["type"], content: string, timeout = 3000) {
    setType(type);
    setContent(content);
    setIsOpen(true);
  }

  function untoast() {
    setIsOpen(false);
  }

  return { toast, untoast, Toaster: () => toasterElement };
}

const Toaster = (props: ToasterProps) => {
  const { type, content, isOpen } = props;

  const bgColor = {
    success: "bg-green-600",
    neutral: "bg-gray-600",
    warning: "bg-yellow-600",
    error: "bg-red-600",
  };

  const textColor = {
    success: "text-green-100",
    neutral: "text-gray-100",
    warning: "text-yellow-100",
    error: "text-red-100",
  };

  return (
    <div
      className={cn(
        "toast w-40 h-8 rounded-lg grid place-items-center absolute left-4 z-10 transition-all duration-500",
        bgColor[type],
        textColor[type]
      )}
      style={{ bottom: isOpen ? "1rem" : "-10rem" }}
    >
      <p className="text-center text-sm">{content}</p>
    </div>
  );
};

export default Toaster;
