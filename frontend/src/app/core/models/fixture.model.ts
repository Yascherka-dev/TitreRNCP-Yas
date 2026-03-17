export interface ApiFixture {
  fixture: {
    id: number;
    referee: string | null;
    timezone: string;
    date: string;
    timestamp: number;
    venue: { id: number | null; name: string | null; city: string | null };
    status: {
      long: string;
      short: string;
      elapsed: number | null;
      extra: number | null;
    };
  };
  league: {
    id: number;
    name: string;
    country: string;
    logo: string;
    flag: string | null;
    season: number;
    round: string;
    standings: boolean;
  };
  teams: {
    home: { id: number; name: string; logo: string; winner: boolean | null };
    away: { id: number; name: string; logo: string; winner: boolean | null };
  };
  goals: { home: number | null; away: number | null };
  score: {
    halftime: { home: number | null; away: number | null };
    fulltime: { home: number | null; away: number | null };
    extratime: { home: number | null; away: number | null };
    penalty: { home: number | null; away: number | null };
  };
}

export interface Match {
  id: string | number;
  date: Date;
  sport: string;
  status: {
    short: string;
    long: string;
    elapsed: number | null;
  };
  league: {
    id: number;
    name: string;
    country: string;
    logo: string;
    round: string;
  };
  home: {
    id: number;
    name: string;
    logo: string;
    countryCode: string;
    countryName: string;
    flag: string;
    goals: number | null;
    winner: boolean | null;
  };
  away: {
    id: number;
    name: string;
    logo: string;
    countryCode: string;
    countryName: string;
    flag: string;
    goals: number | null;
    winner: boolean | null;
  };
}
