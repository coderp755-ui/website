import { createContext, useState, useEffect } from "react";
import api from "../utils/api";

export const SiteContext = createContext();

export const SiteProvider = ({ children }) => {
  const [country, setCountry] = useState(null);
  const [branch, setBranch] = useState(null);

  useEffect(() => {
    api.get("/site-config/").then((res) => {
      setCountry(res.data.country_code);
      setBranch(res.data.branch_slug);
    });
  }, []);

  return (
    <SiteContext.Provider value={{ country, branch }}>
      {children}
    </SiteContext.Provider>
  );
};
