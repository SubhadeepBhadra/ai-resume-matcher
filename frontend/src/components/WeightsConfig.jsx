import React from 'react';
import { Cpu, PlayCircle } from 'lucide-react';

export default function WeightsConfig({ weights, setWeights, parsedJD, uploadedResumes, onRunMatch, isMatching }) {
  return (
    <div className="max-w-2xl mx-auto bg-white border border-slate-200 p-6 rounded-2xl shadow-xs space-y-6">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
          <Cpu className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-base font-bold text-slate-900">Matching Engine Architecture & Weights</h2>
          <p className="text-xs text-slate-500">Configure balance between skills, embeddings, and experience.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 text-xs">
        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div className="flex justify-between text-slate-700 mb-1 font-medium">
            <span>Skill Match:</span>
            <span className="font-mono font-bold text-emerald-700">{Math.round(weights.skills * 100)}%</span>
          </div>
          <input
            type="range" min="0.1" max="0.8" step="0.05"
            value={weights.skills}
            onChange={(e) => setWeights({ ...weights, skills: parseFloat(e.target.value) })}
            className="w-full accent-indigo-600"
          />
        </div>

        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div className="flex justify-between text-slate-700 mb-1 font-medium">
            <span>Semantic Similarity:</span>
            <span className="font-mono font-bold text-indigo-600">{Math.round(weights.semantic * 100)}%</span>
          </div>
          <input
            type="range" min="0.1" max="0.8" step="0.05"
            value={weights.semantic}
            onChange={(e) => setWeights({ ...weights, semantic: parseFloat(e.target.value) })}
            className="w-full accent-indigo-600"
          />
        </div>

        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div className="flex justify-between text-slate-700 mb-1 font-medium">
            <span>Experience Seniority:</span>
            <span className="font-mono font-bold text-amber-700">{Math.round(weights.experience * 100)}%</span>
          </div>
          <input
            type="range" min="0.05" max="0.5" step="0.05"
            value={weights.experience}
            onChange={(e) => setWeights({ ...weights, experience: parseFloat(e.target.value) })}
            className="w-full accent-indigo-600"
          />
        </div>

        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div className="flex justify-between text-slate-700 mb-1 font-medium">
            <span>Education:</span>
            <span className="font-mono font-bold text-purple-700">{Math.round(weights.education * 100)}%</span>
          </div>
          <input
            type="range" min="0.0" max="0.2" step="0.05"
            value={weights.education}
            onChange={(e) => setWeights({ ...weights, education: parseFloat(e.target.value) })}
            className="w-full accent-indigo-600"
          />
        </div>
      </div>

      <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
        <div className="text-xs text-slate-600">
          <div>Role: <strong className="text-slate-900">{parsedJD?.title || 'Senior Full Stack Java Engineer'}</strong></div>
          <div>Resumes: <strong className="text-slate-900">{uploadedResumes.length > 0 ? `${uploadedResumes.length} candidates` : '12 sample resumes ready'}</strong></div>
        </div>

        <button
          onClick={onRunMatch}
          disabled={isMatching}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold flex items-center space-x-2 transition-all cursor-pointer shadow-xs hover:shadow-md"
        >
          <PlayCircle className="w-4 h-4" />
          <span>{isMatching ? 'Computing Match Scores...' : 'Execute AI Matching'}</span>
        </button>
      </div>
    </div>
  );
}
