package com.stuin.irs_scout;

import android.app.Activity;
import android.content.Context;
import android.util.AttributeSet;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Views.Page;
import com.stuin.irs_scout.Views.TeamMenu;

import java.util.List;

class PageManager extends LinearLayout {
    Updater updater;

    private int current = -1;
    private Activity activity;
    private LabelMaker labelMaker;

    PageManager(Context context, AttributeSet attributeSet) {
        super(context, attributeSet);
    }

    void start() {
        //Start Layout
        labelMaker = new LabelMaker(this);
        setVisibility(VISIBLE);
        findViewById(R.id.Status).setVisibility(VISIBLE);
        activity = (Activity) getParent();

        //Setup centering
        LayoutParams lp = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
        setLayoutParams(lp);
        setGravity(Gravity.CENTER);

        //Download layout
        class Layout extends Request {
            @Override
            public void run(List<String> s) {
                labelMaker.pages(s);

                class Tasks extends Request {
                    @Override
                    public void run(List<String> s) {
                        labelMaker.taskMake(s);

                        //Get Match
                        MatchMaker matchMaker;
                        if(MainActivity.position.contains("it")) {
                            matchMaker = new PitMaker(labelMaker.pageManager, activity.findViewById(R.id.Status));
                            TeamMenu teamMenu = (TeamMenu) getChildAt(0);
                            teamMenu.pitMaker = (PitMaker) matchMaker;
                        } else matchMaker = new MatchMaker(labelMaker.pageManager, activity.findViewById(R.id.Status));

                        updater = new Updater(matchMaker, activity.findViewById(R.id.PageStatus));
                    }
                }
                new Tasks().start("/gametasks");
            }
        }
        new Layout().start("/gamelayout");
    }

    void reset() {
        //Set default phase
        if(current != -1) getChildAt(current).setVisibility(GONE);

        current = 0;
        setPage();

        activity.findViewById(R.id.Previous).setVisibility(GONE);
        if(getChildCount() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);
    }

    Page makePage(String name) {
        //Create phase object
        Page page = new Page(getContext(), name);
        if(name.equals("pit")) page = new TeamMenu(getContext());

        page.setVisibility(GONE);
        addView(page);
        return page;
    }

    void nextPage(View view) {
        //Show next phase
        getChildAt(current).setVisibility(GONE);

        //Set shown buttons
        activity.findViewById(R.id.Previous).setVisibility(VISIBLE);
        if(current + 2 == getChildCount()) view.setVisibility(GONE);

        current++;
        setPage();
    }

    void lastPage(View view) {
        //Hide old phase
        getChildAt(current).setVisibility(GONE);

        //Set shown buttons
        activity.findViewById(R.id.Next).setVisibility(VISIBLE);
        if(current == 1) view.setVisibility(GONE);

        //Set new phase
        current--;
        setPage();
    }

    private void setPage() {
        //Show new phase
        getChildAt(current).setVisibility(VISIBLE);

        //Set phase title
        String name =  ((Page) getChildAt(current)).name;
        name = name.substring(0,1).toUpperCase() + name.substring(1);
        ((TextView) activity.findViewById(R.id.PageStatus)).setText(MainActivity.position + ": " + name);

        //Notify server
        if(updater != null) updater.setStatus();
    }
}