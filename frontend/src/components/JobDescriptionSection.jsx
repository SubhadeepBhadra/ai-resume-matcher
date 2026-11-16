import React, { useState } from 'react';
import { FileEdit, Upload, Zap, CheckCircle2, ArrowRight } from 'lucide-react';

export default function JobDescriptionSection({ jdText, setJdText, selectedJdId, setSelectedJdId, parsedJD, setParsedJD, onProceed }) {
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!jdText.trim()) return;
    setLoading(true);
    try {
      const res = await fetch('/api/jd/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: jdText })
      });
      const data = await res.json();
      if (data.job_description) setParsedJD(data.job_description);
    } catch (err) {
      alert('Failed to analyze JD: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 p-5 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-white font-semibold">
            <FileEdit className="w-5 h-5 text-blue-400" />
            <span>Job Description Input</span>
          </div>
        </div>

        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="Paste or upload Job Description..."
          rows={14}
          className="w-full bg-slate-950 text-slate-200 text-xs font-mono p-4 rounded-xl border border-slate-800 focus:outline-none focus:border-blue-500"
        />

        <div className="flex justify-end">
          <button
            onClick={handleAnalyze}
            disabled={loading || !jdText.trim()}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-medium flex items-center space-x-2 transition-all cursor-pointer"
          >
            <Zap className="w-4 h-4" />
            <span>{loading ? 'Extracting...' : 'Analyze JD & Extract Requirements'}</span>
          </button>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl flex flex-col">
        <div className="flex items-center space-x-2 mb-4 text-white font-semibold">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>Extracted Requirements</span>
        </div>

        {parsedJD ? (
          <div className="space-y-4 flex-1 text-xs">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-semibold block">Role</span>
              <span className="text-sm font-bold text-white">{parsedJD.title}</span>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 text-[10px] uppercase font-semibold block">Required Exp</span>
                <span className="text-sm font-bold text-blue-400">{parsedJD.min_experience_years}+ Years</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 text-[10px] uppercase font-semibold block">Education</span>
                <span className="text-sm font-bold text-indigo-400 truncate">{parsedJD.required_education}</span>
              </div>
            </div>
            <div>
              <span className="text-slate-400 text-[10px] uppercase font-semibold block mb-1">
                Extracted Skills ({parsedJD.required_skills?.length || 0})
              </span>
              <div className="flex flex-wrap gap-1 max-h-48 overflow-y-auto">
                {parsedJD.required_skills?.map((s, i) => (
                  <span key={i} className="bg-blue-950/60 text-blue-300 border border-blue-800/40 px-2 py-0.5 rounded text-[11px]">
                    {s}
                  </span>
                ))}
              </div>
            </div>
            <button
              onClick={onProceed}
              className="mt-auto w-full py-2 bg-slate-800 hover:bg-slate-700 text-blue-300 rounded-lg text-xs font-medium flex items-center justify-center space-x-1"
            >
              <span>Next: Batch Resume Upload</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-slate-500 text-xs text-center p-6">
            Click "Analyze JD" to extract requirements, skills taxonomy, and experience.
          </div>
        )}
      </div>
    </div>
  );
}
