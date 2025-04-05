import { ReactNode } from "react";
import "./Layout.css";

const Layout = ({ children }: { children: ReactNode }) => (
  <>
    <div className="navbar-container">
      <nav>
        <h1 className="text-xl font-bold">Privacy Photo Platform</h1>
      </nav>
    </div>
    {children}
  </>
);

export default Layout;
