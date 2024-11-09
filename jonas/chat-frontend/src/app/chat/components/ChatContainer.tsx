'use client'

import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FiLoader as Loader } from "react-icons/fi";

interface Message {
  isVisibleToUser: boolean;
  role: string;
  content: string;
}

interface ChatContainerProps {
  messages: Message[];
  currentMessage: string | null;
  waitingForResponse: boolean;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  currentMessage,
  waitingForResponse,
}) => (
  <div className="chat-outer-container relative pt-14 h-screen overflow-hidden">
    <div className="chat-messages-container overflow-y-scroll h-full pb-28">
      <div className="chat-messages-inner-container max-w-[650px] mx-auto">
        {messages.map((message, index) =>
          message.isVisibleToUser ? (
            <div
              key={index}
              className={`chat-message mb-[1rem] ${
                message.role === "user"
                  ? "user-message w-fit max-w-[300px] lg:max-w-[650px] ml-auto rounded-lg bg-zinc-300 p-1 px-2"
                  : "assistant-message"
              }`}
            >
              <Markdown remarkPlugins={[remarkGfm]}>{message.content}</Markdown>
            </div>
          ) : null
        )}
        {currentMessage && (
          <div className="chat-message mb-[.625rem] assistant-message">
            {currentMessage}
          </div>
        )}
        {waitingForResponse && (
          <div className="pb-8 grid place-items-center">
            <Loader className="animate-spin h-8 w-8 mx-auto" />
          </div>
        )}
      </div>
    </div>
  </div>
);

export default ChatContainer;
