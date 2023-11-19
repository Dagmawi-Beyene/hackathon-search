import { useState } from "react";
import SearchBar from "./components/SearchBar";


function App() {
  const [searchResults, setSearchResults] = useState({hits: []})
  return (
    <section className="flex flex-col items-center p-6">
      <div className="flex flex-col items-center w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4">Meeting transcript Search</h1>
        <div className="flex w-full mb-6">
          <SearchBar setSearchResults={setSearchResults}/>
        </div>
        <ul className="w-full space-y-4">
          {searchResults.hits.map((result: any) => (
                   <li className="flex flex-col p-4 bg-white rounded-md shadow">
                   <p className="text-blue-600 hover:underline mb-2">
                       {`From: ${result.start_time} - ${result.end_time}`}
                   </p>
                   <p className="text-green-600 mb-2">
                       {`Source: ${result.id.split("_")[0]}.json`}
                   </p>
                   <p className="font-semibold text-lg text-gray-700 mb-2">
                       {result.speaker}
                   </p>
                   <p className="text-gray-500 mb-2">
                       {result.transcripts}
                   </p>
                   <p className="text-sm text-gray-500 mb-2">
                       {`Segment: ${result.id.split("_")[1]}`}
                   </p>
            
               </li>
               ))}
          
        </ul>
      </div>
    </section>
  );
}

export default App;
