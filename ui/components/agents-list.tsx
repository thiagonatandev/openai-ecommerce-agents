"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot } from "lucide-react";
import { PanelSection } from "./panel-section";
import type { Agent } from "@/lib/types";

interface AgentsListProps {
  agents: Agent[];
  currentAgent: string;
}

export function AgentsList({ agents, currentAgent }: AgentsListProps) {
  const activeAgent = agents.find((a) => a.name === currentAgent);
  return (
    <PanelSection
      title="Available Agents"
      icon={<Bot className="h-4 w-4 text-teal-200 " />}
      titleStyle="text-slate-100"
    >
      <div className="grid grid-cols-3 gap-3">
        {agents.map((agent) => (
          <Card
            key={agent.name}
            className={`bg-[#2a2a2a] border border-slate-600 transition-all ${
              agent.name === currentAgent ||
              activeAgent?.handoffs.includes(agent.name)
                ? ""
                : "opacity-50 filter grayscale cursor-not-allowed pointer-events-none"
            } ${
              agent.name === currentAgent ? "ring-1 ring-blue-400 shadow-md" : ""
            }`}
          >
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-sm flex items-center text-gray-200">
                {agent.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-1">
              <p className="text-xs font-light text-gray-400">
                {agent.description}
              </p>
              {agent.name === currentAgent && (
                <Badge className="mt-2 bg-blue-400 hover:bg-blue-500 text-white">
                  Active
                </Badge>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </PanelSection>
  );
}