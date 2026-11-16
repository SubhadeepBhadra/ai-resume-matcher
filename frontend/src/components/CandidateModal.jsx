import React, { useState } from 'react';
import { X } from 'lucide-react';

export default function CandidateModal({ candidate, parsedJD, onClose }) {
  const [tab, setTab] = useState('analysis');

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="p-5 border-b border-slate-200 flex justify-between items-center bg-slate-50/60">
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-lg font-bold text-slate-900">{candidate.name}</h3>
              <span className="text-xs bg-white text-slate-700 px-2.5 py-0.5 rounded-full border border-slate-200 font-bold shadow-2xs">Rank #{candidate.rank}</span>
              <span className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded font-bold">{candidate.match_percentage}% Match</span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">{candidate.email} • {candidate.experience_display} • {candidate.education}</p>
          </div>
          <button onClick={onClose} className="p-1 rounded bg-white hover:bg-slate-100 text-slate-500 hover:text-slate-800 border border-slate-200 shadow-2xs cursor-pointer">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex border-b border-slate-200 bg-white text-xs">
          <button
            onClick={() => setTab('analysis')}
            className={`py-2.5 px-4 font-bold border-b-2 cursor-pointer ${tab === 'analysis' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-800'}`}
          >
            Match Breakdown & Reasons
          </button>
          <button
            onClick={() => setTab('skills')}
            className={`py-2.5 px-4 font-bold border-b-2 cursor-pointer ${tab === 'skills' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-800'}`}
          >
            Skills Comparison
          </button>
        </div>

        <div className="p-5 overflow-y-auto flex-1 space-y-4 text-xs">
          {tab === 'analysis' && (
            <>
              <div className="grid grid-cols-4 gap-2">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 text-[10px] uppercase font-bold block">Skill Match (45%)</span>
                  <span className="text-base font-bold text-emerald-700">{candidate.explanation?.metrics_breakdown?.skill_match_percentage}%</span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 text-[10px] uppercase font-bold block">Semantic (35%)</span>
                  <span className="text-base font-bold text-indigo-600">{candidate.explanation?.metrics_breakdown?.semantic_similarity_percentage}%</span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 text-[10px] uppercase font-bold block">Experience (15%)</span>
                  <span className="text-base font-bold text-amber-700">{candidate.explanation?.metrics_breakdown?.experience_alignment_percentage}%</span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 text-[10px] uppercase font-bold block">Education (5%)</span>
                  <span className="text-base font-bold text-purple-700">{candidate.explanation?.metrics_breakdown?.education_score}%</span>
                </div>
              </div>

              <div className="bg-indigo-50/50 border border-indigo-200/80 p-3.5 rounded-xl">
                <span className="font-bold text-indigo-800 block mb-1">Executive Summary</span>
                <p className="text-slate-700 leading-relaxed">{candidate.explanation?.summary}</p>
              </div>

              <div className="bg-emerald-50/50 border border-emerald-200/80 p-3.5 rounded-xl">
                <span className="font-bold text-emerald-800 block mb-1">Key Strengths</span>
                <ul className="space-y-1 text-slate-700">
                  {candidate.explanation?.strengths.map((s, i) => (
                    <li key={i}>• {s}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-amber-50/50 border border-amber-200/80 p-3.5 rounded-xl">
                <span className="font-bold text-amber-800 block mb-1">Identified Gaps & Missing Skills</span>
                <ul className="space-y-1 text-slate-700">
                  {candidate.explanation?.gaps.map((g, i) => (
                    <li key={i}>• {g}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-purple-50/50 border border-purple-200/80 p-3.5 rounded-xl">
                <span className="font-bold text-purple-800 block mb-1">Interview Recommendations</span>
                <ul className="space-y-1 text-slate-700">
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
                <span className="text-emerald-800 font-bold block mb-2">Matched Skills ({candidate.matched_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.matched_skills.map((s, i) => (
                    <span key={i} className="bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded font-semibold">✓ {s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-rose-800 font-bold block mb-2">Missing Skills ({candidate.missing_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.missing_skills.map((s, i) => (
                    <span key={i} className="bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-0.5 rounded font-semibold">✗ {s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-purple-800 font-bold block mb-2">Additional Skills ({candidate.bonus_skills.length})</span>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.bonus_skills.map((s, i) => (
                    <span key={i} className="bg-purple-50 text-purple-700 border border-purple-200 px-2.5 py-0.5 rounded font-medium">+ {s}</span>
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
