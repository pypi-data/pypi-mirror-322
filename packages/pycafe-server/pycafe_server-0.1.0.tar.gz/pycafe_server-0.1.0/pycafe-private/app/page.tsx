"use client";
import * as React from "react";
import { ProjectPageProps } from "@/src/types";
import { getIconByType } from "@/components/dashboard";
import { useTheme } from "@mui/material/styles";
import { Box, Button, Theme, useMediaQuery } from "@mui/material";
import "material-icons/iconfont/material-icons.css";
import { frameworks, settings, tagline } from "@/src/data";
import { useUser } from "@/src/user";
import { CardButton } from "@/app/components/cardbutton";
import Link from "next/link";
import Header from "@/app/components/header";

export const dynamic = "force-static";

function CreateProjectBanner(props: { theme: Theme; isMobile?: boolean; showDescription?: boolean }) {
  const showDescription = props.showDescription ?? false;
  const isMobile = props.isMobile ?? false;
  const darkMode = props.theme.palette.mode === "dark";
  const user = useUser();
  // either no logging in is configured (trial), or the user is an editor
  const canEdit = !user || user.info.is_editor;
  return (
    <div className="create-banner">
      <h2>{canEdit ? "Open the editor to create a new app" : "You are not an editor, and cannot create projects"}</h2>
      <div className="create-buttons">
        {canEdit &&
          settings.frameworks.map((frameworkName) => {
            const framework = frameworks[frameworkName];
            return (
              <a href={`/snippet/${framework.appType}/v1`} key={framework.appType} style={{ textDecoration: "none", color: "unset" }}>
                <CardButton
                  title={framework.name}
                  description={showDescription ? framework.description2 : ""}
                  isMobile={isMobile}
                  image={getIconByType(framework.appType, showDescription, darkMode)}
                  actionIcon="add"
                  disabled={!canEdit}
                />
              </a>
            );
          })}
      </div>
    </div>
  );
}

export default function Page({ params, searchParams }: ProjectPageProps, appview: boolean = false) {
  const theme = useTheme();
  const user = useUser();
  const isMobile = useMediaQuery("(max-width: 1200px)");
  return (
    <>
      {settings.trialmode && (
        <h3>
          PyCafe server is running in trial mode, please obtain a license key at{" "}
          <a href="https://py.cafe/contact" target="_blank">
            PyCafe
          </a>
        </h3>
      )}
      <Header subtitle={tagline} />
      <div className="hero">
        {!settings.requireAuth || user ? <CreateProjectBanner theme={theme} showDescription={true} isMobile={isMobile} /> : null}
        {!settings.requireAuth || user ? null : (
          <Button variant="contained" color="primary" href="/_login">
            Sign in
          </Button>
        )}
      </div>
      {!settings.requireAuth || user ? (
        <div className="framework-container" style={{ width: "800px" }}>
          <Box sx={{ boxShadow: 2, p: 5 }} className="framework-box future-feature" style={{ paddingLeft: "0", paddingRight: "0" }}>
            <div className="vote-container">
              <div className="box-text" style={{ minWidth: "500px" }}>
                <Link href="/view">Open the PyCafe viewer.</Link>
              </div>
            </div>
          </Box>
        </div>
      ) : null}
    </>
  );
  // return <App type="solara" version="v1" />;
  // return <h1>hi</h1>
}
