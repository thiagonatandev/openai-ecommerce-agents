"use client";

import { Bot } from "lucide-react";
import type { Agent, AgentEvent, GuardrailCheck } from "@/lib/types";
import { AgentsList } from "./agents-list";
import { Guardrails } from "./guardrails";
import { ConversationContext } from "./conversation-context";
import { RunnerOutput } from "./runner-output";

interface AgentPanelProps {
  agents: Agent[];
  currentAgent: string;
  events: AgentEvent[];
  guardrails: GuardrailCheck[];
  context: {
    order_number?: string;
    customer_email?: string;
    product_id?: string;
    user_id?: string;
    payment_id?: string;
    tracking_code?: string;
    discount_code?: string;
    return_reason?: string;
  };
}

export function AgentPanel({
  agents,
  currentAgent,
  events,
  guardrails,
  context,
}: AgentPanelProps) {
  const activeAgent = agents.find((a) => a.name === currentAgent);
  const runnerEvents = events.filter((e) => e.type !== "message");

  return (
    <div className="w-3/5 h-full flex flex-col border-r border-slate-600 bg-[#1e1e1e] rounded-xl shadow-md">
      <div className="bg-blue-700 text-white h-12 px-4 flex items-center gap-3 shadow-sm rounded-t-xl border-b border-blue-800">
        <Bot className="h-5 w-5" />
        <h1 className="font-semibold text-sm sm:text-base lg:text-lg">
          Agent View
        </h1>
        <span className="ml-auto text-xs font-light tracking-wide opacity-80">
          Orders&nbsp;Co.
        </span>
      </div>

      <div className="flex-1 text-stone-100 overflow-y-auto p-6 bg-[#1e1e1e]">
        <AgentsList agents={agents} currentAgent={currentAgent} />
        <Guardrails
          guardrails={guardrails}
          inputGuardrails={activeAgent?.input_guardrails ?? []}
        />
        <ConversationContext context={context} />
        <RunnerOutput runnerEvents={runnerEvents} />
      </div>
    </div>
  );
}
