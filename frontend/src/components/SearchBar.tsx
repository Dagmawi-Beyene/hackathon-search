import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from './ui/button'; // import based on your library
import { Input } from './ui/input'; // import based on your library

const SearchBar = ({
    setSearchResults,
    setIsLoading,
}: {
    setSearchResults: (results: any) => void;
    setIsLoading: (isLoading: boolean) => void;

}) => {
  const [query, setQuery] = useState("");
  const [typingTimeout, setTypingTimeout] = useState<any>(0);

  const doSearch = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post("/search", {
        question: query,
      });
      setSearchResults(response.data.search_results);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false); // Set back to false when search is done
    }
  };

  useEffect(() => {
    if (typingTimeout) {
      clearTimeout(typingTimeout);
    }

    if (query) {
      setTypingTimeout(
        setTimeout(() => {
          doSearch();
        }, 1000)
      );
    }
  }, [query]);

  return (
    <div className="flex w-full md:w-[550px] h-11 items-center bg-[#18181b] rounded-full px-4 shadow-lg shadow-black/40 mb-4">
      <div className="flex-none w-8 h-8 rounded-full overflow-hidden bg-[#18181b] flex items-center justify-center mr-2">
        <svg
          className=" h-4 w-4 text-white"
          fill="none"
          height="24"
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          width="24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>
      </div>
      <div className="border-l border-zinc-600 h-full" />
      <div className="flex-grow relative pr-4">
        <Input
          className="flex rounded-md border-input px-3 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none  focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 w-full h-full py-2 bg-[#18181b] text-white placeholder:text-zinc-400 border-0 outline-none focus:outline-none"
          placeholder="Search meeting transcripts..."
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <div className="flex-none w-8 h-8 rounded-full overflow-hidden bg-[#545455] flex items-center justify-center">
        <Button className="p-2" variant="ghost" type="submit">
        <svg
							width="16"
							height="16"
							viewBox="0 0 16 16"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								fill-rule="evenodd"
								clip-rule="evenodd"
								d="M13.5 3V2.25H15V3V10C15 10.5523 14.5522 11 14 11H3.56062L5.53029 12.9697L6.06062 13.5L4.99996 14.5607L4.46963 14.0303L1.39641 10.9571C1.00588 10.5666 1.00588 9.93342 1.39641 9.54289L4.46963 6.46967L4.99996 5.93934L6.06062 7L5.53029 7.53033L3.56062 9.5H13.5V3Z"
								fill="currentColor"
							></path>
						</svg>
        </Button>
      </div>
    </div>
  );
};

export default SearchBar;
