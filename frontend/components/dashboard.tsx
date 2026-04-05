import type { DashboardResponse } from "@/lib/api";
import { CheckInForm } from "@/components/checkin-form";

type Props = {
  data: DashboardResponse;
  onRefresh: () => Promise<void> | void;
  onLogout: () => Promise<void> | void;
};

export function Dashboard({ data, onRefresh, onLogout }: Props) {
  const myScore = data.my_score;
  const buddyScore = data.buddy_score;

  return (
    <main className="page">
      <section className="hero card">
        <div>
          <p className="eyebrow">90-Day Six Pack Accountability</p>
          <h1>Gym Buddy</h1>
          <p className="lead">
            Personal accountability for {data.current_user.name}, shared competition with {data.buddy_user.name},
            and a supportive leaderboard built around consistency.
          </p>
        </div>
        <div className="hero-actions">
          <div className="hero-stat">
            <span>Today</span>
            <strong>{data.generated_for}</strong>
          </div>
          <button className="ghost-button" onClick={() => void onLogout()} type="button">
            Log Out
          </button>
        </div>
      </section>

      <section className="grid two">
        <article className="card">
          <h2>Leaderboard</h2>
          <div className="leaderboard">
            {data.leaderboard.entries.map((entry) => (
              <div key={entry.user_id} className="leader-row">
                <div>
                  <p className="rank">#{entry.rank}</p>
                  <h3>{entry.user_name}</h3>
                </div>
                <div className="leader-metrics">
                  <span>{entry.total_points} pts</span>
                  <span>{entry.current_streak} day streak</span>
                  <span>{entry.score_delta >= 0 ? "+" : ""}{entry.score_delta} delta</span>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="card">
          <h2>Program Rules</h2>
          <ul className="stack">
            <li>Train 6 days per week for up to 90 minutes.</li>
            <li>3 consecutive misses triggers a 30-point penalty and recovery mode.</li>
            <li>Stay sugar-aware and keep meals Tamil vegetarian and protein-focused.</li>
            <li>Abs are revealed by consistency, fat loss, steps, sleep, and gym work together.</li>
          </ul>
        </article>
      </section>

      <section className="grid two">
        <article className="card">
          <div className="card-head">
            <div>
              <p className="eyebrow">My Profile</p>
              <h2>{data.current_user.name}</h2>
            </div>
            <span className="pill">{data.current_user.dietary_preferences.join(" / ")}</span>
          </div>
          <p>{data.current_user.goal}</p>

          {myScore ? (
            <div className="score-grid">
              <div><span>Total</span><strong>{myScore.total}</strong></div>
              <div><span>Steps</span><strong>{myScore.breakdown.steps_activity}</strong></div>
              <div><span>Workout</span><strong>{myScore.breakdown.workout_completion}</strong></div>
              <div><span>Diet</span><strong>{myScore.breakdown.diet_adherence}</strong></div>
              <div><span>Recovery</span><strong>{myScore.breakdown.recovery_checkin}</strong></div>
              <div><span>Penalty</span><strong>{myScore.breakdown.penalties}</strong></div>
            </div>
          ) : null}

          {data.my_coach_insight ? (
            <div className="insight">
              <h3>My Coach Insight</h3>
              <p>{data.my_coach_insight.summary}</p>
              <ul className="stack">
                {data.my_coach_insight.next_actions.map((action) => <li key={action}>{action}</li>)}
              </ul>
            </div>
          ) : null}

          <div>
            <h3>My Milestones</h3>
            <ul className="stack">
              {data.my_milestones.map((milestone) => (
                <li key={milestone.id}>
                  {milestone.title} by {milestone.target_date} for {milestone.bonus_points} pts
                </li>
              ))}
            </ul>
          </div>
        </article>

        <article className="card">
          <div className="card-head">
            <div>
              <p className="eyebrow">Buddy Snapshot</p>
              <h2>{data.buddy_user.name}</h2>
            </div>
            <span className="pill">{data.buddy_user.dietary_preferences.join(" / ")}</span>
          </div>
          <p>{data.buddy_user.goal}</p>

          {buddyScore ? (
            <div className="score-grid">
              <div><span>Total</span><strong>{buddyScore.total}</strong></div>
              <div><span>Steps</span><strong>{buddyScore.breakdown.steps_activity}</strong></div>
              <div><span>Workout</span><strong>{buddyScore.breakdown.workout_completion}</strong></div>
              <div><span>Diet</span><strong>{buddyScore.breakdown.diet_adherence}</strong></div>
              <div><span>Recovery</span><strong>{buddyScore.breakdown.recovery_checkin}</strong></div>
              <div><span>Penalty</span><strong>{buddyScore.breakdown.penalties}</strong></div>
            </div>
          ) : null}

          {data.buddy_coach_insight ? (
            <div className="insight">
              <h3>Buddy Coach Insight</h3>
              <p>{data.buddy_coach_insight.summary}</p>
            </div>
          ) : null}

          <div>
            <h3>Buddy Milestones</h3>
            <ul className="stack">
              {data.buddy_milestones.map((milestone) => (
                <li key={milestone.id}>
                  {milestone.title} by {milestone.target_date} for {milestone.bonus_points} pts
                </li>
              ))}
            </ul>
          </div>
        </article>
      </section>

      <section className="grid two">
        <article className="card">
          <CheckInForm
            onSaved={onRefresh}
            today={data.generated_for}
            userId={data.current_user.id}
            userName={data.current_user.name}
          />
        </article>

        <article className="card">
          <h2>Today’s Focus</h2>
          {data.my_checkin ? (
            <div className="insight">
              <h3>Latest Saved Check-In</h3>
              <p>{data.my_checkin.notes || "No notes saved yet."}</p>
              <p className="muted">
                Mood: {data.my_checkin.mood} · Soreness: {data.my_checkin.soreness} · Workout:{" "}
                {data.my_checkin.workout_completed ? "done" : "missed"}
              </p>
            </div>
          ) : (
            <p className="muted">No check-in saved yet for today. Use the form to record your progress.</p>
          )}
        </article>
      </section>

      <section className="grid two">
        <article className="card">
          <h2>6-Day Workout Plan</h2>
          <p className="lead-small">{data.workout_plan.focus}</p>
          <div className="stack">
            {data.workout_plan.days.map((day) => (
              <div key={day.day} className="day-plan">
                <div className="day-plan-header">
                  <h3>{day.day}</h3>
                  <span>{day.theme} · {day.duration_minutes} min</span>
                </div>
                <ul className="stack compact">
                  {day.exercises.map((exercise) => (
                    <li key={exercise.name}>{exercise.name} - {exercise.sets} x {exercise.reps}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </article>

        <article className="card">
          <h2>Tamil Vegetarian Meal Guidance</h2>
          <div className="stack">
            {data.meal_guidance.map((meal) => (
              <div key={meal.id} className="meal-card">
                <div className="day-plan-header">
                  <h3>{meal.title}</h3>
                  <span>{meal.meal_type}</span>
                </div>
                <p>{meal.items.join(" · ")}</p>
                <p className="muted">Avoid: {meal.avoid.join(", ")}</p>
              </div>
            ))}
          </div>
        </article>
      </section>
    </main>
  );
}
