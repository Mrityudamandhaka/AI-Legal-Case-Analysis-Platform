"use client";
import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [text, setText] = useState("");
  const [clauses, setClauses] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [authenticated, setAuthenticated] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  // Check if user is authenticated on component mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    } else {
      setAuthenticated(true);
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  const handleUpload = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError("");
    setSuccess("");
    setClauses([]);
    setSummary(null);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      
      if (!res.ok) {
        if (res.status === 401) {
          handleLogout();
          return;
        }
        throw new Error(`Failed to upload file: ${res.status} ${res.statusText}`);
      }
      
      const data = await res.json();
      setText(data.content);
      setSuccess("File uploaded and processed successfully!");
    } catch (err: any) {
      console.error("Upload error:", err);
      setError(err.message || "An error occurred while uploading the file");
      setText("");
    } finally {
      setLoading(false);
    }
  };

  const handleExtractClauses = async () => {
    if (!text) {
      setError("Please upload a document first");
      return;
    }

    setExtracting(true);
    setError("");
    setSuccess("");
    setClauses([]);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/extract/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        if (res.status === 401) {
          handleLogout();
          return;
        }
        const errorData = await res.json();
        throw new Error(`Failed to extract clauses: ${errorData.detail || res.statusText}`);
      }

      const data = await res.json();
      setClauses(data.extracted_data.clauses);
      setSuccess("Clauses extracted successfully!");
    } catch (err: any) {
      console.error("Extraction error:", err);
      setError(err.message || "An error occurred while extracting clauses");
    } finally {
      setExtracting(false);
    }
  };

  const handleSummarize = async () => {
    if (!text) {
      setError("Please upload a document first");
      return;
    }

    setSummarizing(true);
    setError("");
    setSuccess("");
    setSummary(null);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/summarize/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        if (res.status === 401) {
          handleLogout();
          return;
        }
        const errorData = await res.json();
        throw new Error(`Failed to summarize document: ${errorData.detail || res.statusText}`);
      }

      const data = await res.json();
      setSummary(data);
      setSuccess("Document summarized successfully!");
    } catch (err: any) {
      console.error("Summarization error:", err);
      setError(err.message || "An error occurred while summarizing the document");
    } finally {
      setSummarizing(false);
    }
  };

  const handleSelectFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Function to get risk color based on score
  const getRiskColor = (score: number) => {
    if (score < 30) return 'bg-green-500';
    if (score < 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Function to get risk text color based on score
  const getRiskTextColor = (score: number) => {
    if (score < 30) return 'text-green-700';
    if (score < 70) return 'text-yellow-700';
    return 'text-red-700';
  };

  // Function to get risk background color based on score
  const getRiskBgColor = (score: number) => {
    if (score < 30) return 'bg-green-100';
    if (score < 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  // Don't render the main content if not authenticated
  if (!authenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center py-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">LawMind</h1>
            <p className="text-xl text-gray-600">AI-Powered Legal Document Analysis</p>
          </div>
          <button 
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300"
          >
            Logout
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Upload Section */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Document Upload</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-4">
              <input 
                type="file" 
                onChange={handleUpload} 
                className="hidden" 
                id="file-upload"
                accept=".pdf,.txt" 
                ref={fileInputRef}
              />
              <div className="flex flex-col items-center justify-center">
                <div className="bg-blue-100 rounded-full p-4 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <p className="text-lg font-medium text-gray-700 mb-2">Upload a legal document</p>
                <p className="text-gray-500 mb-4">PDF or TXT files supported</p>
                <button 
                  onClick={handleSelectFile}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition duration-300"
                >
                  Select File
                </button>
              </div>
            </div>
            
            {loading && (
              <div className="flex items-center justify-center bg-blue-50 p-4 rounded-lg">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
                <p className="text-blue-700 font-medium">Uploading and processing document...</p>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Analysis Tools</h2>
            <div className="space-y-4">
              <button 
                onClick={handleExtractClauses} 
                disabled={!text || extracting}
                className={`w-full py-3 px-4 rounded-lg font-medium transition duration-300 flex items-center justify-center ${
                  !text || extracting 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                    : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                }`}
              >
                {extracting ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Extracting Clauses...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    Extract Clauses
                  </>
                )}
              </button>
              
              <button 
                onClick={handleSummarize} 
                disabled={!text || summarizing}
                className={`w-full py-3 px-4 rounded-lg font-medium transition duration-300 flex items-center justify-center ${
                  !text || summarizing 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                    : 'bg-purple-600 hover:bg-purple-700 text-white'
                }`}
              >
                {summarizing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Analyzing & Scoring...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Summarize & Score Risk
                  </>
                )}
              </button>
            </div>
            
            {(error || success) && (
              <div className={`mt-4 p-4 rounded-lg ${error ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
                <p className={`font-medium ${error ? 'text-red-700' : 'text-green-700'}`}>
                  {error ? `Error: ${error}` : `Success: ${success}`}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Document Content */}
        {text && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Document Content</h2>
            <div className="border rounded-lg p-4 max-h-60 overflow-y-auto bg-gray-50">
              <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm">
                {text}
              </pre>
            </div>
          </div>
        )}

        {/* Risk Analysis Dashboard */}
        {summary && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Risk Analysis Dashboard</h2>
            
            {/* Summary */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Document Summary
              </h3>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-gray-700">{summary.summary}</p>
              </div>
            </div>
            
            {/* Risk Score */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Risk Assessment
              </h3>
              <div className="bg-gray-50 p-6 rounded-lg">
                <div className="flex flex-col md:flex-row items-center justify-between mb-4">
                  <div className="text-center mb-4 md:mb-0">
                    <div className={`text-5xl font-bold ${getRiskTextColor(summary.risk_score)}`}>
                      {summary.risk_score}
                    </div>
                    <div className="text-gray-600">Risk Score (0-100)</div>
                  </div>
                  
                  <div className="flex-1 md:mx-8 mb-4 md:mb-0">
                    <div className="w-full bg-gray-200 rounded-full h-6">
                      <div 
                        className={`h-6 rounded-full ${getRiskColor(summary.risk_score)} transition-all duration-1000 ease-out`}
                        style={{ width: `${summary.risk_score}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600 mt-1">
                      <span>Low Risk</span>
                      <span>High Risk</span>
                    </div>
                  </div>
                  
                  <div className={`px-4 py-2 rounded-full text-lg font-semibold ${getRiskBgColor(summary.risk_score)} ${getRiskTextColor(summary.risk_score)}`}>
                    {summary.risk_level}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Key Points and Recommendations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                  Key Points
                </h3>
                <div className="bg-yellow-50 p-4 rounded-lg">
                  <ul className="space-y-2">
                    {summary.key_points.map((point: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="flex-shrink-0 h-5 w-5 text-yellow-600 mr-2">•</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Recommendations
                </h3>
                <div className="bg-green-50 p-4 rounded-lg">
                  <ul className="space-y-2">
                    {summary.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="flex-shrink-0 h-5 w-5 text-green-600 mr-2">✓</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Extracted Clauses */}
        {clauses.length > 0 && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Extracted Clauses</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {clauses.map((clause, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow bg-gray-50">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-bold text-lg text-gray-800">{clause.title}</h3>
                    <span className="inline-block bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                      {clause.type}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">{clause.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}