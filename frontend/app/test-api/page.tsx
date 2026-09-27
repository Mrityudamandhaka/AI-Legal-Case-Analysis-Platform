"use client";
import { useState } from "react";

export default function TestAPI() {
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const testBackendConnection = async () => {
    setLoading(true);
    setResult("");
    
    try {
      const response = await fetch("http://localhost:8000/");
      const data = await response.json();
      setResult(`Success: ${JSON.stringify(data)}`);
    } catch (error: any) {
      setResult(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">API Test</h1>
        
        <button
          onClick={testBackendConnection}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300"
        >
          {loading ? "Testing..." : "Test Backend Connection"}
        </button>
        
        {result && (
          <div className="mt-6 p-4 bg-gray-100 rounded-lg">
            <p className="text-gray-700">{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}