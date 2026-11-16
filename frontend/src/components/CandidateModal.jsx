import React, { useState } from 'react';
import { X, CheckCircle, AlertTriangle, HelpCircle, Clock } from 'lucide-react';

export default function CandidateModal({ candidate, parsedJD, onClose }) {
  const [tab, setTab] = useState('analysis');

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="p-5 border-b border-slate-800 flex justify-between items-center bg-slate-950">
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-lg font-bold text-white">{candidate.name}</h3>
              <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-mono">Rank #{candidate.rank}</span>
              <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold">{candidate.match_percentage}% Match</span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">{candidate.email} • {candidate.experience_display} • {candidate.education}</p>
          </div>
          <button onClick={onClose} className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex border-b border-slate-800 bg-slate-950/40 text-xs">
          <button
            onClick={() => setTab('analysis')}
            className={`py-2.5 px-4 font-semibold border-b-2 ${tab === 'analysis' ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400'}`}
          >
            Match Breakdown & Reasons
          </button>
          <button
            onClick={() => setTab('skills')}
            className={`py-2.5 px-4 font-semibold border-b-2 ${tab === 'skills' ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400'}`}
          >
            Skills Comparison
          </button>
        </div>

        <div className="p-5 overflow-y-auto flex-1 space-y-4 text-xs">
          {tab === 'analysis' && (
            <>
              <div className="grid grid-cols-4 gap-2">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-400 text-[10px] block">Skill Match (45%)</span>
                  <span className="text-base font-bold text-emerald-400">{candidate.explanation?.metrics_breakdown?.skill_match_percentage}%</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-400 text-[10px] block">Semantic (35%)</span>
                  <span className="text-base font-bold text-blue-400">{candidate.explanation?.metrics_breakdown?.semantic_similarity_percentage}%</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-400 text-[10px] block">Experience (15%)</span>
                  <span className="text-base font-bold text-amber-400">{candidate.explanation?.metrics_breakdown?.experience_alignment_percentage}%</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-400 text-[10px] block">Education (5%)</span>
                  <span className="text-base font-bold text-purple-400">{candidate.explanation?.metrics_breakdown?.education_score}%</span>
                </div>
              </div>

              <div className="bg-blue-950/30 border border-blue-900/40 p-3.5 rounded-xl">
                <span className="font-semibold text-blue-300 block mb-1">Executive Summary</span>
                <p className="text-slate-300 leading-relaxed">{candidate.explanation?.summary}</p>
              </div>

              <div className="bg-emerald-950/20 border border-emerald-900/40 p-3.5 rounded-xl">
                <span className="font-semibold text-emerald-300 block mb-1">Key Strengths</span>
                <ul className="space-y-1 text-slate-300">
                  {candidate.explanation?.strengths.map((s, i) => (
                    <li key={i}>• {s}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-amber-950/20 border border-amber-900/40 p-3.5 rounded-xl">
                <span className="font-semibold text-amber-300 block mb-1">Identified Gaps & Missing Skills</span>
                <ul className="space-y-1 text-slate-300">
                  {candidate.explanation?.gaps.map((g, i) => (
                    <li key={i}>• {g}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-purple-950/20 border border-purple-900/40 p-3.5 rounded-xl">
                <span className="font-semibold text-purple-300 block mb-1">Interview Recommendations</span>
                <ul className="space-y-1 text-slate-300">
                  {candidate.explanation?.interview_focus.map((q, i) => (
                    <li key={i}>• {q}</li>
                  ))}
                </ul>
              </div>
            </>
          )}

          {tab === 'skills' && (
            <div className="space-y-4">
              <div>
                <span className="text-emerald-400 font-semibold block mb-2">Matched Skills ({candidate.matched_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.matched_skills.map((s, i) => (
                    <span key={i} className="bg-emerald-950/60 text-emerald-300 border border-emerald-800/50 px-2 py-0.5 rounded">✓ {s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-rose-400 font-semibold block mb-2">Missing Skills ({candidate.missing_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.missing_skills.map((s, i) => (
                    <span key={i} className="bg-rose-950/60 text-rose-300 border border-rose-800/50 px-2 py-0.5 rounded">✗ {s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-purple-400 font-semibold block mb-2">Additional Skills ({candidate.bonus_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.bonus_skills.map((s, i) => (
                    <span key={i} className="bg-purple-950/50 text-purple-300 border border-purple-800/40 px-2 py-0.5 rounded">+ {s}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
