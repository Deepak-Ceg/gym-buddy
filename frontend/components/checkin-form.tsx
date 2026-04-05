"use client";

import { useState, useTransition } from "react";

import { postCheckIn, type CheckInSubmission } from "@/lib/api";

type Props = {
  userId: string;
  userName: string;
  today: string;
  onSaved: () => Promise<void> | void;
};

const defaultState = {
  workout_completed: true,
  recovery_completed: true,
  mood: "motivated",
  soreness: "medium",
  notes: "",
  voice_transcript: "",
  sugar_free: true,
  low_fried_food: true,
  hydration_goal_met: true,
  protein_focus_met: true,
  fiber_focus_met: true
};

export function CheckInForm({ userId, userName, today, onSaved }: Props) {
  const [isPending, startTransition] = useTransition();
  const [form, setForm] = useState(defaultState);
  const [message, setMessage] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);

    const payload: CheckInSubmission = {
      user_id: userId,
      date: today,
      workout_completed: form.workout_completed,
      recovery_completed: form.recovery_completed,
      mood: form.mood,
      soreness: form.soreness,
      notes: form.notes,
      voice_transcript: form.voice_transcript || undefined,
      diet: {
        sugar_free: form.sugar_free,
        low_fried_food: form.low_fried_food,
        hydration_goal_met: form.hydration_goal_met,
        protein_focus_met: form.protein_focus_met,
        fiber_focus_met: form.fiber_focus_met
      }
    };

    try {
      await postCheckIn(payload);
      setMessage(`Saved today's check-in for ${userName}.`);
      startTransition(() => {
        void onSaved();
      });
    } catch {
      setMessage(`Could not save today's check-in for ${userName}.`);
    }
  }

  function toggle(name: keyof typeof defaultState) {
    return (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = event.target.checked;
      setForm((current) => ({ ...current, [name]: value }));
    };
  }

  return (
    <form className="checkin-form" onSubmit={handleSubmit}>
      <div className="checkin-form-head">
        <div>
          <p className="eyebrow">My Daily Check-In</p>
          <h3>{userName}</h3>
        </div>
        <span className="pill">{today}</span>
      </div>

      <div className="checkin-grid">
        <label className="toggle">
          <input checked={form.workout_completed} onChange={toggle("workout_completed")} type="checkbox" />
          <span>Workout completed</span>
        </label>
        <label className="toggle">
          <input checked={form.recovery_completed} onChange={toggle("recovery_completed")} type="checkbox" />
          <span>Recovery done</span>
        </label>
        <label className="toggle">
          <input checked={form.sugar_free} onChange={toggle("sugar_free")} type="checkbox" />
          <span>Sugar-free</span>
        </label>
        <label className="toggle">
          <input checked={form.low_fried_food} onChange={toggle("low_fried_food")} type="checkbox" />
          <span>Low fried food</span>
        </label>
        <label className="toggle">
          <input checked={form.hydration_goal_met} onChange={toggle("hydration_goal_met")} type="checkbox" />
          <span>Hydration goal met</span>
        </label>
        <label className="toggle">
          <input checked={form.protein_focus_met} onChange={toggle("protein_focus_met")} type="checkbox" />
          <span>Protein focus met</span>
        </label>
        <label className="toggle">
          <input checked={form.fiber_focus_met} onChange={toggle("fiber_focus_met")} type="checkbox" />
          <span>Fiber focus met</span>
        </label>
      </div>

      <div className="field-row">
        <label>
          <span>Mood</span>
          <select
            value={form.mood}
            onChange={(event) => setForm((current) => ({ ...current, mood: event.target.value }))}
          >
            <option value="motivated">Motivated</option>
            <option value="steady">Steady</option>
            <option value="tired">Tired</option>
            <option value="stressed">Stressed</option>
          </select>
        </label>
        <label>
          <span>Soreness</span>
          <select
            value={form.soreness}
            onChange={(event) => setForm((current) => ({ ...current, soreness: event.target.value }))}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </label>
      </div>

      <label>
        <span>Notes</span>
        <textarea
          rows={3}
          value={form.notes}
          onChange={(event) => setForm((current) => ({ ...current, notes: event.target.value }))}
          placeholder="What went well today? What was hard?"
        />
      </label>

      <label>
        <span>Voice transcript</span>
        <textarea
          rows={2}
          value={form.voice_transcript}
          onChange={(event) => setForm((current) => ({ ...current, voice_transcript: event.target.value }))}
          placeholder="Paste or type a short voice check-in summary."
        />
      </label>

      <button className="submit-button" disabled={isPending} type="submit">
        {isPending ? "Saving..." : "Save Check-In"}
      </button>

      {message ? <p className="form-message">{message}</p> : null}
    </form>
  );
}
