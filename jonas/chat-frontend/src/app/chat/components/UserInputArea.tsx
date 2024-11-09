"use client";

import { FiPaperclip as PaperClipIcon } from "react-icons/fi";
import { FaArrowCircleUp as ArrowUp } from "react-icons/fa";
import { DOCUMENT_UPLOAD_ENDPOINT } from "@/utils/api";
import { ChangeEvent, useContext, useState } from "react";
import { ChatContext } from "@/providers/ChatProvider";
import { cn } from "@/lib/utils";

interface UserInputAreaProps {
  userInput: string;
  setUserInput: (value: string) => void;
  callChatEndpoint: (message: string) => void;
}

const UserInputArea: React.FC<UserInputAreaProps> = ({
  userInput,
  setUserInput,
  callChatEndpoint,
}) => {
  const [uploadedFiles, setUploadedFiles] = useState<FileList | null>(null);

  const handleFileInput = async (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    setUploadedFiles(files);
    if (files) {
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i], files[i].name);
      }
      const response = await fetch(DOCUMENT_UPLOAD_ENDPOINT, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        console.log("Files uploaded successfully.");
      } else {
        console.log("Error uploading files. Status code:" + response.status);
      }
    }
  };

  const { bot } = useContext(ChatContext);

  // @ts-ignore
  const submitInputIfEnter = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      callChatEndpoint(userInput);
    }
  };

  return (
    <form>
      <div className="user-input-area max-w-[800px] mx-auto">
        <div className="user-input-container rounded-lg h-24 bg-[#f4f4f4] p-2 flex flex-col">
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={submitInputIfEnter}
            placeholder="Escreva sua mensagem aqui"
            className="user-input resize-none outline-none bg-transparent flex-1"
          ></textarea>
          <div className="input-controls-container flex flex-row items-center">
            <FileInputControls
              handleFileInput={handleFileInput}
              uploadedFiles={uploadedFiles}
              isShown={bot === "bot_document"}
            />
            <button className="header-1 ml-auto">
              <ArrowUp
                size={24}
                fill={"#444"}
                onClick={() => callChatEndpoint(userInput)}
              />
            </button>
          </div>
        </div>
      </div>
    </form>
  );
};

interface FileInputProps {
  handleFileInput: (e: ChangeEvent<HTMLInputElement>) => void;
  uploadedFiles: FileList | null;
  isShown: boolean;
}

const FileInputControls: React.FC<FileInputProps> = ({
  handleFileInput,
  uploadedFiles,
  isShown,
}) => {
  return (
    <div
      className={cn(
        "flex items-center transition-all duration-300 relative",
        isShown ? "scale-100 opacity-100" : "scale-0 opacity-0"
      )}
    >
      <label className="p-1 cursor-pointer" htmlFor="input-file">
        <PaperClipIcon size={20} stroke={"#444"} />
      </label>
      <input
        type="file"
        multiple={true}
        onChange={handleFileInput}
        className="hidden"
        id="input-file"
      />
      <div className="uploaded-files-area ml-2 space-x-1">
        {uploadedFiles &&
          [...uploadedFiles].map((file) => {
            return <UploadedFilePill filename={file.name} />;
          })}
      </div>
    </div>
  );
};

const UploadedFilePill = ({ filename }: { filename: string }) => (
  <div className="pill-uploaded-file rounded-2xl w-28 h-8 p-1 inline-flex items-center bg-sky-600">
    <div className="upload-progress-circle rounded-full w-5 h-5 bg-white"></div>
    <p className="text-xs font-semibold text-white ml-1">{filename}</p>
  </div>
);

export default UserInputArea;
