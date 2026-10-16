from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analytics import analytics_engine

app = FastAPI(title="IPL 2025 Data Story API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to IPL 2025 Data API"}

@app.get("/api/kpis")
def get_kpis():
    return analytics_engine.get_dashboard_kpis()

@app.get("/api/team-performance")
def get_team_performance():
    return analytics_engine.get_team_performance()

@app.get("/api/top-batters")
def get_top_batters():
    return analytics_engine.get_top_batters()

@app.get("/api/top-bowlers")
def get_top_bowlers():
    return analytics_engine.get_top_bowlers()

@app.get("/api/venue-analysis")
def get_venue_analysis():
    return analytics_engine.get_venue_analysis()

@app.get("/api/player-profile/{player_name}")
def get_player_profile(player_name: str):
    return analytics_engine.get_player_profile(player_name)

@app.get("/api/distribution/{column_name}")
def get_distribution(column_name: str):
    return analytics_engine.get_distribution(column_name)

@app.get("/api/grouped-distribution/{metric}/{group_by}")
def get_grouped_distribution(metric: str, group_by: str):
    return analytics_engine.get_grouped_distribution(metric, group_by)

@app.get("/api/category-distribution/{category}")
def get_category_distribution(category: str):
    return analytics_engine.get_category_distribution(category)

@app.get("/api/data-quality-report")
def get_data_quality_report():
    return analytics_engine.get_data_quality_report()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
