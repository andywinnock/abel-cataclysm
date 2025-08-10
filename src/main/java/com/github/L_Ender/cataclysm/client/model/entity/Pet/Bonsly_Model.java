package com.github.L_Ender.cataclysm.client.model.entity.Pet;

import com.github.L_Ender.cataclysm.entity.Pet.Bonsly_Entity;
import com.github.L_Ender.lionfishapi.client.model.tools.AdvancedEntityModel;
import com.github.L_Ender.lionfishapi.client.model.tools.AdvancedModelBox;
import com.github.L_Ender.lionfishapi.client.model.Animations.ModelAnimator;
import com.github.L_Ender.lionfishapi.client.model.tools.BasicModelPart;
import com.google.common.collect.ImmutableList;
import net.minecraft.client.Minecraft;
import net.minecraft.util.Mth;

public class Bonsly_Model extends AdvancedEntityModel<Bonsly_Entity> {
    private final AdvancedModelBox bonsly;
    private final AdvancedModelBox body;
    private final AdvancedModelBox torso;
    private final AdvancedModelBox stem;
    private final AdvancedModelBox stem2;
    private final AdvancedModelBox leaf_left;
    private final AdvancedModelBox leaf_right;
    private final AdvancedModelBox leaf_middle;
    private final AdvancedModelBox eye_left;
    private final AdvancedModelBox eyelid_left;
    private final AdvancedModelBox eye_right;
    private final AdvancedModelBox eyelid_right;
    private final AdvancedModelBox mouth_open;
    private final AdvancedModelBox mouth_closed;
    private final AdvancedModelBox leg_left;
    private final AdvancedModelBox leg_left2;
    private final AdvancedModelBox foot_left;
    private final AdvancedModelBox leg_right;
    private final AdvancedModelBox leg_right2;
    private final AdvancedModelBox foot_right;
    private ModelAnimator animator;

    public Bonsly_Model() {
        texWidth = 64;
        texHeight = 64;

        bonsly = new AdvancedModelBox(this);
        bonsly.setRotationPoint(0.0F, 24.0F, 0.0F);

        body = new AdvancedModelBox(this);
        body.setRotationPoint(0.0F, -9.0F, 0.0F);
        bonsly.addChild(body);

        torso = new AdvancedModelBox(this);
        torso.setRotationPoint(0.0F, 4.0F, 0.0F);
        body.addChild(torso);
        torso.setTextureOffset(0, 12).addBox(-4.0F, -7.5F, -4.0F, 8.0F, 9.0F, 8.0F, 0.0F, false);
        torso.setTextureOffset(0, 0).addBox(-5.0F, -2.5F, -5.0F, 10.0F, 2.0F, 10.0F, 0.0F, false);

        stem = new AdvancedModelBox(this);
        stem.setRotationPoint(0.0F, -6.5F, -3.5F);
        torso.addChild(stem);
        setRotationAngle(stem, -0.1745F, 0.0F, 0.0F);
        stem.setTextureOffset(26, 23).addBox(-3.0F, -5.0F, 0.0F, 6.0F, 4.0F, 6.0F, 0.0F, false);

        stem2 = new AdvancedModelBox(this);
        stem2.setRotationPoint(0.0F, -4.0F, 4.0F);
        stem.addChild(stem2);
        setRotationAngle(stem2, 0.1745F, 0.0F, 0.0F);
        stem2.setTextureOffset(0, 0).addBox(-2.5F, -8.0F, 0.0F, 5.0F, 7.0F, 0.0F, 0.0F, false);

        leaf_left = new AdvancedModelBox(this);
        leaf_left.setRotationPoint(2.0F, -3.5F, -0.5F);
        stem2.addChild(leaf_left);
        leaf_left.setTextureOffset(30, 0).addBox(-0.5F, -3.5F, -2.5F, 5.0F, 5.0F, 5.0F, 0.0F, false);

        leaf_right = new AdvancedModelBox(this);
        leaf_right.setRotationPoint(-2.0F, -3.5F, -0.5F);
        stem2.addChild(leaf_right);
        leaf_right.setTextureOffset(0, 29).addBox(-4.5F, -3.5F, -2.5F, 5.0F, 5.0F, 5.0F, 0.0F, false);

        leaf_middle = new AdvancedModelBox(this);
        leaf_middle.setRotationPoint(0.0F, -7.0F, -0.5F);
        stem2.addChild(leaf_middle);
        leaf_middle.setTextureOffset(32, 12).addBox(-2.5F, -5.5F, -2.5F, 5.0F, 5.0F, 5.0F, 0.0F, false);

        eye_left = new AdvancedModelBox(this);
        eye_left.setRotationPoint(2.25F, -3.75F, -4.0125F);
        torso.addChild(eye_left);
        eye_left.setTextureOffset(6, 12).addBox(-0.5F, -2.0F, -0.0025F, 1.0F, 2.0F, 0.0F, 0.0F, false);
        eye_left.setTextureOffset(24, 15).addBox(-1.0F, -2.5F, 0.0025F, 2.0F, 3.0F, 0.0F, 0.0F, false);

        eyelid_left = new AdvancedModelBox(this);
        eyelid_left.setRotationPoint(0.0F, -1.0F, 0.6025F);
        eye_left.addChild(eyelid_left);
        eyelid_left.setTextureOffset(0, 16).addBox(-1.0F, -1.5F, -0.5F, 2.0F, 3.0F, 1.0F, 0.01F, false);

        eye_right = new AdvancedModelBox(this);
        eye_right.setRotationPoint(-2.25F, -3.75F, -4.0125F);
        torso.addChild(eye_right);
        eye_right.setTextureOffset(8, 7).addBox(-0.5F, -2.0F, -0.0025F, 1.0F, 2.0F, 0.0F, 0.0F, false);
        eye_right.setTextureOffset(0, 7).addBox(-1.0F, -2.5F, 0.0025F, 2.0F, 3.0F, 0.0F, 0.0F, false);

        eyelid_right = new AdvancedModelBox(this);
        eyelid_right.setRotationPoint(0.0F, -1.0F, 0.6025F);
        eye_right.addChild(eyelid_right);
        eyelid_right.setTextureOffset(0, 12).addBox(-1.0F, -1.5F, -0.5F, 2.0F, 3.0F, 1.0F, 0.01F, false);

        mouth_open = new AdvancedModelBox(this);
        mouth_open.setRotationPoint(0.0F, -3.0F, -3.9125F);
        torso.addChild(mouth_open);
        
        // Add mouth open geometry
        AdvancedModelBox cube_r1 = new AdvancedModelBox(this);
        cube_r1.setRotationPoint(0.0F, -1.0F, 0.0025F);
        mouth_open.addChild(cube_r1);
        setRotationAngle(cube_r1, 0.0F, 0.0F, 0.1309F);
        cube_r1.setTextureOffset(8, 9).addBox(0.0F, 0.0F, 0.0F, 1.0F, 1.0F, 0.0F, 0.0F, false);
        
        AdvancedModelBox cube_r2 = new AdvancedModelBox(this);
        cube_r2.setRotationPoint(0.0F, -1.0F, 0.0025F);
        mouth_open.addChild(cube_r2);
        setRotationAngle(cube_r2, 0.0F, 0.0F, -0.1309F);
        cube_r2.setTextureOffset(6, 14).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 1.0F, 0.0F, 0.0F, false);

        mouth_closed = new AdvancedModelBox(this);
        mouth_closed.setRotationPoint(0.0F, -3.0F, -4.0125F);
        torso.addChild(mouth_closed);
        
        // Add mouth closed geometry
        AdvancedModelBox cube_r3 = new AdvancedModelBox(this);
        cube_r3.setRotationPoint(0.0F, -1.0F, 0.0025F);
        mouth_closed.addChild(cube_r3);
        setRotationAngle(cube_r3, 0.0F, 0.0F, 0.1309F);
        cube_r3.setTextureOffset(6, 15).addBox(0.0F, 0.0F, 0.0F, 1.0F, 1.0F, 0.0F, 0.0F, false);
        
        AdvancedModelBox cube_r4 = new AdvancedModelBox(this);
        cube_r4.setRotationPoint(0.0F, -1.0F, 0.0025F);
        mouth_closed.addChild(cube_r4);
        setRotationAngle(cube_r4, 0.0F, 0.0F, -0.1309F);
        cube_r4.setTextureOffset(6, 16).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 1.0F, 0.0F, 0.0F, false);

        leg_left = new AdvancedModelBox(this);
        leg_left.setRotationPoint(3.0F, 4.5F, 0.0F);
        body.addChild(leg_left);
        leg_left.setTextureOffset(12, 39).addBox(-1.5F, -1.5F, -1.5F, 3.0F, 3.0F, 3.0F, 0.0F, false);

        leg_left2 = new AdvancedModelBox(this);
        leg_left2.setRotationPoint(0.0F, 1.5F, -0.5F);
        leg_left.addChild(leg_left2);
        leg_left2.setTextureOffset(24, 12).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 2.0F, 1.0F, 0.0F, false);

        foot_left = new AdvancedModelBox(this);
        foot_left.setRotationPoint(0.0F, 1.5F, 0.5F);
        leg_left2.addChild(foot_left);
        foot_left.setTextureOffset(34, 33).addBox(-1.5F, -0.5F, -2.5F, 3.0F, 2.0F, 4.0F, 0.0F, false);

        leg_right = new AdvancedModelBox(this);
        leg_right.setRotationPoint(-3.0F, 4.5F, 0.0F);
        body.addChild(leg_right);
        leg_right.setTextureOffset(0, 39).addBox(-1.5F, -1.5F, -1.5F, 3.0F, 3.0F, 3.0F, 0.0F, false);

        leg_right2 = new AdvancedModelBox(this);
        leg_right2.setRotationPoint(0.0F, 1.5F, -0.5F);
        leg_right.addChild(leg_right2);
        leg_right2.setTextureOffset(4, 7).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 2.0F, 1.0F, 0.0F, false);

        foot_right = new AdvancedModelBox(this);
        foot_right.setRotationPoint(0.0F, 1.5F, 0.5F);
        leg_right2.addChild(foot_right);
        foot_right.setTextureOffset(20, 33).addBox(-1.5F, -0.5F, -2.5F, 3.0F, 2.0F, 4.0F, 0.0F, false);
        
        animator = ModelAnimator.create();
        this.updateDefaultPose();
    }

    @Override
    public void setupAnim(Bonsly_Entity entityIn, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        this.resetToDefaultPose();
        animator.update(entityIn);
        
        float partialTick = Minecraft.getInstance().getFrameTime();
        float sitProgress = entityIn.prevSitProgress + (entityIn.sitProgress - entityIn.prevSitProgress) * partialTick;
        
        // Sitting animation (sleep pose)
        progressRotationPrev(torso, sitProgress, (float)Math.toRadians(-7.5F), (float)Math.toRadians(-2.5F), (float)Math.toRadians(5.0F), 5f);
        progressPositionPrev(torso, sitProgress, 0.0F, -3.0F, 0.0F, 5f);
        
        // Leg positions for sleep
        progressRotationPrev(leg_left, sitProgress, (float)Math.toRadians(-85.0F), (float)Math.toRadians(-50.0F), 0.0F, 5f);
        progressPositionPrev(leg_left, sitProgress, 1.0F, -2.25F, -2.0F, 5f);
        
        progressRotationPrev(leg_right, sitProgress, (float)Math.toRadians(-82.5F), (float)Math.toRadians(50.0F), 0.0F, 5f);
        progressPositionPrev(leg_right, sitProgress, -1.0F, -2.25F, -2.0F, 5f);
        
        // Close eyes when sitting
        progressPositionPrev(eyelid_left, sitProgress, 0.0F, 0.0F, -0.1F, 5f);
        progressPositionPrev(eyelid_right, sitProgress, 0.0F, 0.0F, -0.1F, 5f);
        
        // Walking animation
        float walkSpeed = 1.5F;
        float walkDegree = 1.0F;
        float walkSwingAmount = limbSwingAmount * (1F - 0.2F * sitProgress);
        
        // Body sway while walking
        this.walk(torso, walkSpeed, walkDegree * 0.1F, false, 0F, 0.05F, limbSwing, walkSwingAmount);
        this.swing(torso, walkSpeed, walkDegree * 0.15F, false, 0F, 0.0F, limbSwing, walkSwingAmount);
        
        // Leg movement
        this.walk(leg_left, walkSpeed, walkDegree * 0.4F, true, 1F, 0.0F, limbSwing, walkSwingAmount);
        this.walk(leg_right, walkSpeed, walkDegree * 0.4F, false, 1F, 0.0F, limbSwing, walkSwingAmount);
        this.walk(leg_left2, walkSpeed, walkDegree * 0.6F, false, 1.5F, 0.6F, limbSwing, walkSwingAmount);
        this.walk(leg_right2, walkSpeed, walkDegree * 0.6F, true, 1.5F, 0.6F, limbSwing, walkSwingAmount);
        
        // Idle breathing and plant movement
        float idleSpeed = 0.05F;
        float idleDegree = 0.05F;
        this.walk(torso, idleSpeed * 3.0F, idleDegree, false, 0F, 0.0F, ageInTicks, 1.0f);
        this.swing(torso, idleSpeed * 1.5F, idleDegree, false, 0F, 0.0F, ageInTicks, 1.0f);
        
        // Stem and leaf movement
        this.swing(stem2, idleSpeed * 2.0F, 0.15F, false, 0F, 0.0F, ageInTicks, 1.0f);
        this.swing(leaf_left, idleSpeed * 1.2F, 0.1F, false, 0F, 0.0F, ageInTicks, 1.0f);
        this.swing(leaf_right, idleSpeed * 1.3F, 0.1F, true, 1F, 0.0F, ageInTicks, 1.0f);
        this.walk(leaf_middle, idleSpeed * 0.8F, 0.05F, false, 0F, 0.0F, ageInTicks, 1.0f);
        
        // Head rotation
        this.bonsly.rotateAngleX += headPitch * ((float) Math.PI / 180F);
        this.bonsly.rotateAngleY += netHeadYaw * ((float) Math.PI / 180F);
    }

    @Override
    public Iterable<BasicModelPart> parts() {
        return ImmutableList.of(bonsly);
    }

    @Override
    public Iterable<AdvancedModelBox> getAllParts() {
        return ImmutableList.of(bonsly, body, torso, stem, stem2, leaf_left, leaf_right, leaf_middle,
                eye_left, eyelid_left, eye_right, eyelid_right, mouth_open, mouth_closed,
                leg_left, leg_left2, foot_left, leg_right, leg_right2, foot_right);
    }

    public void setRotationAngle(AdvancedModelBox advancedModelBox, float x, float y, float z) {
        advancedModelBox.rotateAngleX = x;
        advancedModelBox.rotateAngleY = y;
        advancedModelBox.rotateAngleZ = z;
    }
}