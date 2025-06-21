"use client";

import { PanelSection } from "./panel-section";
import { Card, CardContent } from "@/components/ui/card";
import { BookText } from "lucide-react";

interface ConversationContextProps {
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

export function ConversationContext({ context }: ConversationContextProps) {
  return (
    <PanelSection
      title="Conversation Context"
      icon={<BookText className="h-4 w-4 text-teal-200" />}
      titleStyle="text-slate-100"
    >
      <Card className="bg-gradient-to-r from-[#2a2a2a] to-[#1e1e1e] border border-slate-600 shadow-sm">
        <CardContent className="p-3">
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(context).map(([key, value]) => (
              <div
                key={key}
                className="flex items-center gap-2 bg-[#333333] p-2 rounded-md border border-slate-600 shadow-sm transition-all"
              >
                <div className={`w-2 h-2 rounded-full ${value ? 'bg-teal-200' :'bg-teal-700'}`}></div>
                <div className="text-xs">
                  <span className="text-stone-100 font-light">{key}:</span>{" "}
                  <span
                    className={
                      value
                        ? "text-stone-100 font-light"
                        : "text-stone-400 italic"
                    }
                  >
                    {value || "null"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </PanelSection>
  );
}