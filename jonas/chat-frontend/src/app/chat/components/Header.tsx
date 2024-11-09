"use client";

import Dropdown from "@/components/custom/Dropdown";
import { Dispatch, SetStateAction } from "react";

interface HeaderProps {
  chatOption: string;
  setChatOption: Dispatch<SetStateAction<string>>;
  modelName: string;
  setModelName: Dispatch<SetStateAction<string>>;
}

const Header: React.FC<HeaderProps> = (props) => {
  const { chatOption, setChatOption, modelName, setModelName } = props;

  const chatOptions = [
    { value: "bot_document", label: "Document Bot" },
    { value: "bot_internet", label: "Internet Bot" },
    { value: "bot_sql", label: "SQL Bot" },
  ];

  const modelOptions = [
    { value: "gpt-4o-mini", label: "gpt-4o-mini" },
    { value: "gpt-4o", label: "gpt-4o" },
    { value: "meta/llama-3.2-3b-instruct", label: "llama-3.2-3b-instruct" },
    { value: "meta/llama-3.1-70b-instruct", label: "llama-3.1-70b-instruct" },
  ];

  return (
    <>
      <h1 className="text-center text-lg font-bold">Chat</h1>
      <div className="flex flex-row gap-4 items-center">
        <Dropdown
          placeholder="Assistente"
          handleChange={setChatOption}
          value={chatOption}
          items={chatOptions}
        />
        <Dropdown
          placeholder="Modelo"
          handleChange={setModelName}
          value={modelName}
          items={modelOptions}
        />
      </div>
    </>
  );
};

export default Header;
