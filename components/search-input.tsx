"use client";

import { useState, useEffect } from "react";
import { SearchIcon } from "lucide-react";
import { Input } from "./ui/input"; // Adjust the import path according to your project structure
import { useDebounce } from "@/hooks/use-debounce";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import qs from "query-string";

const SearchInput = () => {
  const [value, setValue] = useState("");
  const debounceValue = useDebounce(value);
  const [recommendations, setRecommendations] = useState<any[]>([]);

  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const currentCategoryId = searchParams.get("categoryId");

  useEffect(() => {
    const url = qs.stringifyUrl(
      {
        url: pathname,
        query: {
          categoryId: currentCategoryId,
          title: debounceValue,
        },
      },
      { skipEmptyString: true, skipNull: true }
    );

    router.push(url);
  }, [debounceValue, router, pathname, currentCategoryId]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("Submitting form with value:", value);

    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ course_title: value }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Received recommendations:", data);
        setRecommendations(data);
      } else {
        console.error("Failed to get recommendations", response.statusText);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <div className="relative">
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <SearchIcon className="h-4 w-4 text-slate-600" />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full md:w-[300px] rounded-full bg-slate-100 focus-visible"
          placeholder="Search for a course"
        />
        <button type="submit" className="btn-primary">Search</button>
      </form>

      <h2>Recommendations:</h2>
      <div>
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>{rec.course_title}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SearchInput;
