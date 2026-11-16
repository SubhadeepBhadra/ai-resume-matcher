import React, { useState } from 'react';
import { FileEdit, Zap, CheckCircle2, ArrowRight } from 'lucide-react';

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
      <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-slate-900 font-bold">
            <FileEdit className="w-5 h-5 text-indigo-600" />
            <span>Job Description Input</span>
          </div>
        </div>

        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="Paste or upload Job Description..."
          rows={14}
          className="w-full bg-slate-50 text-slate-800 text-xs font-mono p-4 rounded-xl border border-slate-200 focus:outline-none focus:border-indigo-500 focus:bg-white resize-none"
        />

        <div className="flex justify-end">
          <button
            onClick={handleAnalyze}
            disabled={loading || !jdText.trim()}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all cursor-pointer shadow-xs"
          >
            <Zap className="w-4 h-4" />
            <span>{loading ? 'Extracting...' : 'Analyze JD & Extract Requirements'}</span>
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col">
        <div className="flex items-center space-x-2 mb-4 pb-3 border-b border-slate-100 text-slate-900 font-bold">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          <span>Extracted Requirements</span>
        </div>

        {parsedJD ? (
          <div className="space-y-4 flex-1 text-xs">
            <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
              <span className="text-slate-500 text-[10px] uppercase font-bold block">Role</span>
              <span className="text-sm font-bold text-slate-900">{parsedJD.title}</span>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                <span className="text-slate-500 text-[10px] uppercase font-bold block">Required Exp</span>
                <span className="text-sm font-bold text-indigo-600">{parsedJD.min_experience_years}+ Years</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                <span className="text-slate-500 text-[10px] uppercase font-bold block">Education</span>
                <span className="text-sm font-bold text-slate-800 truncate">{parsedJD.required_education}</span>
              </div>
            </div>
            <div>
              <span className="text-slate-500 text-[10px] uppercase font-bold block mb-1">
                Extracted Skills ({parsedJD.required_skills?.length || 0})
              </span>
              <div className="flex flex-wrap gap-1 max-h-48 overflow-y-auto">
                {parsedJD.required_skills?.map((s, i) => (
                  <span key={i} className="bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded text-[11px] font-semibold">
                    {s}
                  </span>
                ))}
              </div>
            </div>
            <button
              onClick={onProceed}
              className="mt-auto w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold flex items-center justify-center space-x-1 shadow-xs cursor-pointer"
            >
              <span>Next: Batch Resume Upload</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-slate-400 text-xs text-center p-6">
            Click "Analyze JD" to extract requirements, skills taxonomy, and experience.
          </div>
        )}
      </div>
    </div>
  );
}
