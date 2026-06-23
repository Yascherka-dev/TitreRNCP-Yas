export interface Match {
  id: string;
  date: Date;
  sport: string;
  status: {
    short: string;
    long: string;
    elapsed: number | null;
  };
  league: {
    id: number;
    leagueId?: number;
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
  venue?: string;
  thumbUrl?: string;
}
