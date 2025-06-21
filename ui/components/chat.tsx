"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import type { Message } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

interface ChatProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

export function Chat({ messages, onSendMessage, isLoading }: ChatProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [inputText, setInputText] = useState("");
  const [isComposing, setIsComposing] = useState(false);
  const [finalTranscript, setFinalTranscript] = useState("");
  
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    isMicrophoneAvailable
  } = useSpeechRecognition();

  useEffect(() => {
    if (transcript) {
      setInputText(prev => `${prev} ${transcript}`.trim());
      resetTranscript();
    }
  }, [transcript]);

  useEffect(() => {
    if (!listening && transcript) {
      setFinalTranscript(transcript);
      console.log('Final transcript:', transcript);
    }
  }, [listening, transcript]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "instant" });
  }, [messages, isLoading]);

  const handleSend = useCallback(() => {
    if (!inputText.trim()) return;
    onSendMessage(inputText);
    setInputText("");
    resetTranscript();
    setFinalTranscript("");
  }, [inputText, onSendMessage, resetTranscript]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey && !isComposing) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend, isComposing]
  );

  const toggleListening = useCallback(() => {
    if (listening) {
      SpeechRecognition.stopListening();
    } else {
      resetTranscript();
      setFinalTranscript("");
      SpeechRecognition.startListening({
        continuous: true,
        language: 'en-US'
      });
    }
  }, [listening, resetTranscript]);

  return (
    <div className="flex flex-col h-full flex-1 bg-[#1e1e1e] text-gray-200 border border-slate-600 rounded-xl shadow-md">
      <div className="bg-blue-700 text-white h-12 px-4 flex items-center rounded-t-xl border-b border-slate-600">
        <h2 className="font-semibold text-sm sm:text-base lg:text-lg">
          Customer View
        </h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto min-h-0 md:px-4 pt-4 pb-20">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex mb-5 text-sm ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-[16px] px-4 py-2 font-light max-w-[80%] ${
                msg.role === "user"
                  ? "bg-[#2e2e2e] text-white ml-4 md:ml-24 rounded-br-[4px]"
                  : "bg-[#3a3a3a] text-gray-100 mr-4 md:mr-24 rounded-bl-[4px]"
              }`}
            >
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex mb-5 text-sm justify-start pl-4">
            <div className="h-3 w-3 bg-gray-400 rounded-full animate-pulse" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      
      <div className="p-2 md:px-4 bg-[#1e1e1e]">
        <div className="flex items-center">
          <div className="flex w-full items-center pb-4 md:pb-1">
            <div className="flex w-full flex-row items-center gap-2 rounded-2xl p-2.5 bg-[#2a2a2a] border border-slate-600 shadow-sm transition-colors">
              <textarea
                id="prompt-textarea"
                tabIndex={0}
                dir="auto"
                rows={1}
                placeholder="Message..."
                className="flex-1 resize-none overflow-hidden border-0 focus:outline-none text-sm bg-transparent text-gray-100 px-2 py-1"
                style={{ minHeight: "2rem", maxHeight: "150px" }}
                value={inputText}
                onChange={(e) => {
                  setInputText(e.target.value);
                  e.currentTarget.style.height = "auto";
                  e.currentTarget.style.height = `${e.currentTarget.scrollHeight}px`;
                }}
                onKeyDown={handleKeyDown}
                onCompositionStart={() => setIsComposing(true)}
                onCompositionEnd={() => setIsComposing(false)}
              />

              {/* Microphone button */}
              <button
                className={`flex h-8 w-8 items-center justify-center rounded-full ${
                  listening ? 'bg-red-600' : 'bg-black'
                } text-white hover:opacity-80 transition-colors focus:outline-none`}
                onClick={toggleListening}
                disabled={!isMicrophoneAvailable}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11h-2z" />
                </svg>
              </button>

              {/* Send button */}
              <button
                disabled={!inputText.trim()}
                className="flex h-8 w-8 items-center justify-center rounded-full bg-black text-white hover:opacity-80 disabled:bg-gray-500 disabled:text-gray-400 transition-colors focus:outline-none"
                onClick={handleSend}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="32"
                  height="32"
                  fill="none"
                  viewBox="0 0 32 32"
                >
                  <path
                    fill="currentColor"
                    fillRule="evenodd"
                    d="M15.192 8.906a1.143 1.143 0 0 1 1.616 0l5.143 5.143a1.143 1.143 0 0 1-1.616 1.616l-3.192-3.192v9.813a1.143 1.143 0 0 1-2.286 0v-9.813l-3.192 3.192a1.143 1.143 0 1 1-1.616-1.616z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
