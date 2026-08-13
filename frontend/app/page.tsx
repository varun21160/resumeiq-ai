"use client";

import { ChangeEvent, useState } from "react";

interface ResumeData {
  id: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  version: number;
  parsing_status: string;
  created_at: string;
}

interface AnalysisResult {
  id?: string;
  resume_id?: string;
  overall_score: number;
  category_scores: {
    skills?: number;
    experience?: number;
    projects?: number;
    education?: number;
    certifications?: number;
    resume_quality?: number;
    [key: string]: number | undefined;
  };
  analysis?: Record<string, unknown>;
  recommendations?: string[];
}

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [jobDescription, setJobDescription] = useState("");

  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const [uploadMessage, setUploadMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);

  const [token, setToken] = useState("");

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(file.type)) {
      setErrorMessage("Only PDF and DOCX files are supported.");
      setResumeFile(null);
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setErrorMessage("File size must be less than 5 MB.");
      setResumeFile(null);
      return;
    }

    setErrorMessage("");
    setUploadMessage("");
    setResumeFile(file);
  };

  const uploadResume = async () => {
    if (!resumeFile) {
      setErrorMessage("Please select a resume first.");
      return;
    }

    if (!token.trim()) {
      setErrorMessage(
        "Please enter your access token before uploading.",
      );
      return;
    }

    setUploading(true);
    setErrorMessage("");
    setUploadMessage("");

    try {
      const formData = new FormData();

      formData.append("file", resumeFile);

      const response = await fetch(
        `${API_BASE_URL}/resumes/upload`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token.trim()}`,
          },
          body: formData,
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail || "Resume upload failed.",
        );
      }

      setResume(data);

      setUploadMessage(
        "Resume uploaded and parsed successfully.",
      );
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to upload resume.",
      );
    } finally {
      setUploading(false);
    }
  };

  const analyzeResume = async () => {
    if (!resume) {
      setErrorMessage(
        "Please upload a resume before starting the analysis.",
      );
      return;
    }

    if (!jobDescription.trim()) {
      setErrorMessage(
        "Please enter the job description.",
      );
      return;
    }

    if (!token.trim()) {
      setErrorMessage(
        "Please enter your access token.",
      );
      return;
    }

    setAnalyzing(true);
    setErrorMessage("");
    setAnalysis(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/ats/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token.trim()}`,
          },
          body: JSON.stringify({
            resume_id: resume.id,
            job_description: jobDescription.trim(),
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail || "ATS analysis failed.",
        );
      }

      setAnalysis(data);
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to analyze resume.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  const scoreClass = (score: number) => {
    if (score >= 80) {
      return "text-emerald-600";
    }

    if (score >= 60) {
      return "text-amber-500";
    }

    return "text-red-500";
  };

  const formatScore = (score?: number) => {
    if (typeof score !== "number") {
      return 0;
    }

    return Math.round(score);
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-white/10 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              ResumeIQ AI
            </h1>

            <p className="text-sm text-slate-400">
              AI-powered resume & ATS analysis
            </p>
          </div>

          <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-300">
            Backend Connected
          </div>
        </div>
      </header>

      {/* Main */}
      <section className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10">
          <p className="mb-3 text-sm font-medium uppercase tracking-widest text-cyan-400">
            Resume Analysis Platform
          </p>

          <h2 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
            Know exactly how your resume performs against a job.
          </h2>

          <p className="mt-4 max-w-2xl text-lg leading-8 text-slate-400">
            Upload your resume, provide a job description,
            and get an ATS score with category-level insights
            and recommendations.
          </p>
        </div>

        {/* Token */}
        <div className="mb-8 rounded-2xl border border-white/10 bg-white/5 p-6">
          <h3 className="mb-2 text-lg font-semibold">
            Authentication
          </h3>

          <p className="mb-4 text-sm text-slate-400">
            Enter the JWT access token returned by your login API.
          </p>

          <input
            type="password"
            value={token}
            onChange={(event) =>
              setToken(event.target.value)
            }
            placeholder="Paste your access token"
            className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-sm outline-none transition focus:border-cyan-400"
          />
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Resume Upload */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-7 shadow-2xl">
            <div className="mb-6">
              <span className="text-sm font-medium text-cyan-400">
                STEP 01
              </span>

              <h3 className="mt-2 text-2xl font-semibold">
                Upload Resume
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Upload a PDF or DOCX resume. Maximum file size
                is 5 MB.
              </p>
            </div>

            <label className="flex min-h-48 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-600 bg-slate-900/60 px-6 text-center transition hover:border-cyan-400 hover:bg-slate-900">
              <div className="mb-4 text-4xl">
                📄
              </div>

              <p className="font-medium">
                {resumeFile
                  ? resumeFile.name
                  : "Choose your resume"}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                PDF or DOCX • Maximum 5 MB
              </p>

              <input
                type="file"
                accept=".pdf,.docx"
                className="hidden"
                onChange={handleFileChange}
              />
            </label>

            <button
              type="button"
              onClick={uploadResume}
              disabled={uploading || !resumeFile}
              className="mt-5 w-full rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {uploading
                ? "Uploading..."
                : "Upload Resume"}
            </button>

            {resume && (
              <div className="mt-5 rounded-xl border border-emerald-400/20 bg-emerald-400/10 p-4">
                <p className="font-medium text-emerald-300">
                  ✓ Resume uploaded
                </p>

                <p className="mt-1 text-sm text-slate-300">
                  {resume.original_filename}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Parsing status: {resume.parsing_status}
                </p>
              </div>
            )}
          </div>

          {/* JD */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-7 shadow-2xl">
            <div className="mb-6">
              <span className="text-sm font-medium text-cyan-400">
                STEP 02
              </span>

              <h3 className="mt-2 text-2xl font-semibold">
                Job Description
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Paste the job description you want your resume
                evaluated against.
              </p>
            </div>

            <textarea
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(event.target.value)
              }
              placeholder="Paste the complete job description here..."
              className="min-h-48 w-full resize-none rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-sm leading-6 outline-none transition focus:border-cyan-400"
            />

            <button
              type="button"
              onClick={analyzeResume}
              disabled={
                analyzing ||
                !resume ||
                !jobDescription.trim()
              }
              className="mt-5 w-full rounded-xl bg-white px-5 py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {analyzing
                ? "Analyzing Resume..."
                : "Analyze Resume"}
            </button>
          </div>
        </div>

        {/* Messages */}
        {uploadMessage && (
          <div className="mt-6 rounded-xl border border-emerald-400/20 bg-emerald-400/10 px-5 py-4 text-sm text-emerald-300">
            {uploadMessage}
          </div>
        )}

        {errorMessage && (
          <div className="mt-6 rounded-xl border border-red-400/20 bg-red-400/10 px-5 py-4 text-sm text-red-300">
            {errorMessage}
          </div>
        )}

        {/* Results */}
        {analysis && (
          <section className="mt-12">
            <div className="mb-7">
              <p className="text-sm font-medium uppercase tracking-widest text-cyan-400">
                Analysis Complete
              </p>

              <h3 className="mt-2 text-3xl font-bold">
                ATS Analysis Results
              </h3>
            </div>

            {/* Overall Score */}
            <div className="mb-8 rounded-3xl border border-white/10 bg-white/5 p-8">
              <div className="grid gap-8 md:grid-cols-[220px_1fr] md:items-center">
                <div className="flex h-48 w-48 flex-col items-center justify-center rounded-full border-8 border-cyan-400/30 bg-slate-900">
                  <span
                    className={`text-5xl font-bold ${scoreClass(
                      analysis.overall_score,
                    )}`}
                  >
                    {formatScore(
                      analysis.overall_score,
                    )}
                  </span>

                  <span className="mt-1 text-sm text-slate-400">
                    / 100
                  </span>
                </div>

                <div>
                  <h4 className="text-2xl font-semibold">
                    Overall ATS Score
                  </h4>

                  <p className="mt-3 max-w-2xl leading-7 text-slate-400">
                    This score represents the combined performance
                    of your resume across skills, experience,
                    projects, education, certifications and resume
                    quality.
                  </p>
                </div>
              </div>
            </div>

            {/* Category Scores */}
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(
                analysis.category_scores || {},
              ).map(([category, score]) => (
                <div
                  key={category}
                  className="rounded-2xl border border-white/10 bg-white/5 p-6"
                >
                  <p className="text-sm capitalize text-slate-400">
                    {category.replaceAll("_", " ")}
                  </p>

                  <div className="mt-3 flex items-end justify-between">
                    <span
                      className={`text-3xl font-bold ${scoreClass(
                        score ?? 0,
                      )}`}
                    >
                      {formatScore(score)}
                    </span>

                    <span className="text-sm text-slate-500">
                      / 100
                    </span>
                  </div>

                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-cyan-400 transition-all"
                      style={{
                        width: `${Math.min(
                          100,
                          Math.max(0, score ?? 0),
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            {/* Recommendations */}
            <div className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-7">
              <h4 className="text-2xl font-semibold">
                Recommendations
              </h4>

              {analysis.recommendations &&
              analysis.recommendations.length > 0 ? (
                <div className="mt-5 space-y-3">
                  {analysis.recommendations.map(
                    (recommendation, index) => (
                      <div
                        key={`${recommendation}-${index}`}
                        className="flex gap-3 rounded-xl border border-white/10 bg-slate-900/60 p-4"
                      >
                        <span className="text-cyan-400">
                          →
                        </span>

                        <p className="text-sm leading-6 text-slate-300">
                          {recommendation}
                        </p>
                      </div>
                    ),
                  )}
                </div>
              ) : (
                <p className="mt-4 text-slate-400">
                  No recommendations were generated.
                </p>
              )}
            </div>
          </section>
        )}
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 px-6 py-8">
        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-3 text-sm text-slate-500 sm:flex-row">
          <p>
            © 2026 ResumeIQ AI
          </p>

          <p>
            AI-powered resume intelligence platform
          </p>
        </div>
      </footer>
    </main>
  );
}