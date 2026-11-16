import React, { useState, useMemo } from 'react';
import { Search, Download, ChevronRight } from 'lucide-react';

export default function CandidateTable({ candidates, onSelectCandidate, searchQuery, setSearchQuery, jobTitle }) {
  const [sortField, setSortField] = useState('rank');
  const [sortAsc, setSortAsc] = useState(true);

  const getScoreBadge = (score) => {
    if (score >= 80) return 'bg-emerald-50 text-emerald-700 border border-emerald-200/80';
    if (score >= 65) return 'bg-indigo-50 text-indigo-700 border border-indigo-200/80';
    if (score >= 50) return 'bg-amber-50 text-amber-700 border border-amber-200/80';
    return 'bg-rose-50 text-rose-700 border border-rose-200/80';
  };

  const filtered = useMemo(() => {
    let list = [...candidates];
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter(c =>
        c.name.toLowerCase().includes(q) ||
        c.matched_skills.some(s => s.toLowerCase().includes(q))
      );
    }
    list.sort((a, b) => {
      const valA = a[sortField];
      const valB = b[sortField];
      return sortAsc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });
    return list;
  }, [candidates, searchQuery, sortField, sortAsc]);

  const handleExportCSV = () => {
    if (!candidates.length) return;
    const headers = ['Rank', 'Candidate', 'Experience', 'Match %', 'Matched Skills'];
    const rows = candidates.map(c => [c.rank, `"${c.name}"`, `"${c.experience_display}"`, `${c.match_percentage}%`, `"${c.matched_skills.join(', ')}"`]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encoded = encodeURI(csvContent);
    const link = document.createElement('a');
    link.href = encoded;
    link.download = `Candidate_Ranking_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
  };

  return (
    <div className="space-y-4">
      <div className="bg-white border border-slate-200 p-4 rounded-2xl shadow-xs flex flex-col sm:flex-row justify-between items-center gap-3">
        <div>
          <h2 className="text-base font-bold text-slate-900">Candidate Ranking Dashboard</h2>
          <p className="text-xs text-slate-500">Ranked against: <span className="text-indigo-600 font-semibold">{jobTitle || 'Role'}</span></p>
        </div>
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-60">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search candidate or skill..."
              className="bg-slate-50 text-slate-900 text-xs pl-9 pr-3 py-2 rounded-xl border border-slate-200 w-full focus:outline-none focus:border-indigo-500 focus:bg-white"
            />
          </div>
          <button
            onClick={handleExportCSV}
            className="px-3 py-2 bg-white hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-semibold border border-slate-200 shadow-2xs flex items-center space-x-1 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50/80 text-slate-500 uppercase tracking-wider text-[11px] font-bold border-b border-slate-200">
            <tr>
              <th className="py-3 px-4 w-12 cursor-pointer" onClick={() => { setSortField('rank'); setSortAsc(!sortAsc); }}>Rank</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('name'); setSortAsc(!sortAsc); }}>Candidate</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('experience_years'); setSortAsc(!sortAsc); }}>Experience</th>
              <th className="py-3 px-4 cursor-pointer" onClick={() => { setSortField('match_percentage'); setSortAsc(!sortAsc); }}>Match %</th>
              <th className="py-3 px-4">Matched Skills</th>
              <th className="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filtered.map((c) => (
              <tr
                key={c.id}
                onClick={() => onSelectCandidate(c)}
                className="hover:bg-slate-50/70 transition-colors cursor-pointer group"
              >
                <td className="py-3.5 px-4 font-bold text-slate-700">#{c.rank}</td>
                <td className="py-3.5 px-4 font-bold text-slate-900 group-hover:text-indigo-600">{c.name}</td>
                <td className="py-3.5 px-4 text-slate-700 font-medium">{c.experience_display}</td>
                <td className="py-3.5 px-4">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${getScoreBadge(c.match_percentage)}`}>
                    {c.match_percentage}%
                  </span>
                </td>
                <td className="py-3.5 px-4">
                  <div className="flex flex-wrap gap-1 max-w-md">
                    {c.matched_skills.slice(0, 4).map((s, i) => (
                      <span key={i} className="bg-emerald-50 text-emerald-700 border border-emerald-200/80 px-2 py-0.5 rounded text-[10px] font-semibold">
                        {s}
                      </span>
                    ))}
                    {c.matched_skills.length > 4 && (
                      <span className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[10px]">+{c.matched_skills.length - 4} more</span>
                    )}
                  </div>
                </td>
                <td className="py-3.5 px-4 text-right">
                  <button className="px-2.5 py-1 bg-white hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200 rounded text-xs font-semibold inline-flex items-center space-x-1 shadow-2xs">
                    <span>Inspect</span>
                    <ChevronRight className="w-3 h-3" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
